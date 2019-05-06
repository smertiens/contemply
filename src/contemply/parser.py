#
# Contemply - A code generator that creates boilerplate files from templates
#
# Copyright (C) 2019  Sean Mertiens
# For more information on licensing see LICENSE file
#

import os
import re

import contemply.cli as cli
from colorama import Fore, Style
from contemply.interpreter import *
from contemply.tokenizer import *


class TemplateContext:
    """
    This class holds all information regarding the template and it's parsing process as well as
    the text that should be parsed.
    """

    def __init__(self):
        self._data = {}
        self._text = ''
        self._outputfile = ''
        self._filename = ''
        self._line = 0
        self._pos = 0

    def set_text(self, text):
        self._text = text

    def text(self):
        return self._text

    def set_filename(self, val):
        self._filename = val

    def set_line(self, val):
        self._line = val

    def set_pos(self, val):
        self._pos = val

    def filename(self):
        return self._filename

    def line(self):
        return self._line

    def pos(self):
        return self._pos

    def set_outputfile(self, file):
        self._outputfile = file

    def outputfile(self):
        return self._outputfile

    def set(self, k, v):
        self._data[k] = v

    def get(self, k):
        return self._data[k]

    def has(self, k):
        return k in self._data

    def get_all(self):
        return self._data

    def set_position(self, line, col):
        self.set_line(line)
        self.set_pos(col)

    def process_variables(self, text):

        def check_and_replace(match):
            varname = match.group(1)[1:]  # strip trailing $

            if not self.has(varname):
                raise ParserError('Unknown variable: "{0}"'.format(varname), self)
            else:
                val = self.get(varname)

                if not isinstance(val, str):
                    val = str(val)

                return '{0}{1}'.format(val, match.group(2))

        p = re.compile(r'(\$[\w_]+)(\s|\W|$)', re.MULTILINE)
        text = p.sub(check_and_replace, text)

        return text


class Parser:
    """
    This class will do the actual parsing. It needs a Tokenizer instance and will then create
    an AST from the input tokens that can be interpreted using the Interpreter.
    """
    CMD_LINE_IDENTIFIER = '#:'
    CONTEMPLY_COMMENT = '#%'

    def __init__(self, tokenizer, ctx):
        self._token = None
        self._tokenizer = tokenizer
        self._ctx = ctx

        self._conditions = []

    def _raise_error(self, msg):
        raise ParserError(msg, self._ctx)

    def get_logger(self):
        return logging.getLogger(self.__module__)

    def parse(self):
        root = self._consume_template()
        return root

    def _consume_template(self):

        node = Template()

        # Consume template line by line
        for i in range(0, len(self._ctx.text())):
            self._ctx.set_position(i, 0)
            self._tokenizer.update_position()

            if self._tokenizer.get_chr() + self._tokenizer.lookahead() == self.CONTEMPLY_COMMENT:
                continue
            elif self._tokenizer.get_chr() + self._tokenizer.lookahead() != self.CMD_LINE_IDENTIFIER:
                node.children.append(self._consume_content_line())
            else:
                self._token = self._tokenizer.get_next_token()
                node.children.append(self._consume_cmd_line())

        return node

    def _consume_next_token(self, ttype):
        if self._token.type() == ttype:
            return self._tokenizer.get_next_token()
        else:
            raise ParserError('Unexpected token, got ' + self._token.type() + ' expected ' + ttype, self._ctx)

    def _consume_cmd_line(self):
        self._token = self._consume_next_token(CMD_LINE_START)
        statement = self._consume_statement()
        return CommandLine(statement)

    def _consume_symbol(self):
        name = self._token.value()
        self._token = self._consume_next_token(SYMBOL)

        if self._token.type() == LPAR:
            node = self._consume_function(name)
        elif self._token.type() in [ASSIGN, ASSIGN_PLUS]:
            node = self._consume_assignment(name)
        else:
            node = Variable(name)

        return node

    def _consume_assignment(self, name):
        assignment_type = self._token.type()
        self._token = self._consume_next_token(assignment_type)
        value = self._consume_expression()
        return Assignment(name, value, assignment_type)

    def _consume_value(self):
        node = None
        if self._token.type() == SYMBOL:
            node = self._consume_symbol()
        elif self._token.type() == STRING:
            node = String(self._token.value())
            self._token = self._consume_next_token(STRING)
        elif self._token.type() == INTEGER:
            node = Num(self._token.value())
            self._token = self._consume_next_token(INTEGER)
        elif self._token.type() == LSQRBR:
            node = self._consume_list()
        else:
            self._raise_error('Unexpected token-type: ' + self._token.type())
        return node

    def _consume_statement(self):
        if self._token.type() == SYMBOL:
            node = self._consume_symbol()
        elif self._token.type() == IF:
            node = self._consume_if_block()
            self._conditions.append(node)
        elif self._token.type() == ELSE:
            try:
                last_condition = self._conditions.pop()
                node = Else(last_condition.condition)
                self._token = self._consume_next_token(ELSE)
                self._conditions.append(node)
            except IndexError:
                raise ParserError("Unexpected token: ELSE", self._ctx)

        elif self._token.type() == ENDIF:
            try:
                self._conditions.pop()
            except IndexError:
                raise ParserError("Unexpected token: ENDIF", self._ctx)

            self._token = self._consume_next_token(ENDIF)
            node = Endif()

        elif self._token.type() == WHILE:
            self._token = self._consume_next_token(WHILE)
            node = While(self._consume_expression(True))

        elif self._token.type() == ENDWHILE:
            node = Endwhile()

        elif self._token.type() == FOR:
            self._token = self._consume_next_token(FOR)
            itemvar = self._consume_symbol()
            self._token = self._consume_next_token(SYMBOL)
            listvar = self._consume_symbol()
            node = For(listvar, itemvar)

        elif self._token.type() == ENDFOR:
            node = Endfor()

        else:
            raise ParserError('Unknown block start: ' + self._token.type(), self._ctx)

        return node

    def _consume_expression(self, condition_testing=False):

        lval = None
        op = None
        rval = None

        if self._token.type() in [STRING, INTEGER]:
            # Consume primitive type
            lval = self._consume_value()
        elif self._token.type() == LSQRBR:
            # Consume list
            lval = self._consume_list()
        elif self._token.type() == SYMBOL:
            # Consume function/builtin/variable
            lval = self._consume_symbol()
        else:
            raise ParserError("Unexpected left value: " + self._token.type(), self._ctx)

        if self._token.type() in OPERATORS:
            op = self._token.value()
            self._token = self._consume_next_token(self._token.type())
        else:
            if condition_testing:
                # short form expression, assume operator == and rval == True
                return SimpleExpression(lval, '==', Variable('True'))
            else:
                return lval

        if self._token.type() in [STRING, INTEGER]:
            # Consume primitive type
            rval = self._consume_value()
        elif self._token.type() == LSQRBR:
            # Consume list
            rval = self._consume_list()
        elif self._token.type() == SYMBOL:
            # Consume function/builtin/variable
            rval = self._consume_symbol()
        else:
            raise ParserError("Unexpected right value: " + self._token.type(), self._ctx)

        return SimpleExpression(lval, op, rval)

    def _consume_if_block(self):

        self._token = self._consume_next_token(IF)
        cond = self._consume_expression()
        node = If(cond)

        return node

    def _consume_content_line(self, prepend=None):
        line = self._tokenizer.get_raw('\n')

        if prepend is not None:
            line = prepend + line

        self._token = self._tokenizer.get_next_token()
        return ContentLine(line)

    def _consume_argument_list(self):
        node = ArgumentList()
        while self._token.type() != RPAR:
            if self._token.type() == EOF or self._token.type() == NEWLINE:
                raise ParserError("Unexpected token in argument list: " + self._token.type(), self._ctx)

            if self._token.type() == COMMA:
                self._token = self._consume_next_token(COMMA)
            else:
                node.children.append(self._consume_value())

        return node

    def _consume_function(self, funcname):
        self._token = self._consume_next_token(LPAR)
        args = self._consume_argument_list()
        self._token = self._consume_next_token(RPAR)
        return Function(funcname, args)

    def _consume_list(self):
        self._token = self._consume_next_token(LSQRBR)
        node = List()
        while self._token.type() != RSQRBR:
            if self._token.type() == COMMA:
                self._token = self._consume_next_token(COMMA)
            else:
                node.children.append(self._consume_value())

        self._token = self._consume_next_token(RSQRBR)
        return node


class TemplateParser:
    """
    This is the frontend class used for TemplateParsing.
    It will set up a TemplateContext and split the input text up in
    separate lines before handing it to the _parse function.
    """

    OUTPUTMODE_CONSOLE, OUTPUTMODE_FILE = 0, 1

    def __init__(self):
        self._ctx = TemplateContext()
        self._output_mode = self.OUTPUTMODE_FILE

    def get_logger(self):
        return logging.getLogger(self.__module__)

    def get_template_context(self):
        return self._ctx

    def set_output_mode(self, mode):
        self._output_mode = mode

    def parse_file(self, filename):
        self._ctx.set_filename(os.path.basename(filename))

        with open(filename, 'r') as f:
            lines = []
            for line in f:
                lines.append(line)
            self._ctx.set_text(lines)

        return self.parse()

    def parse(self, text=None):
        if text is not None:
            self._ctx.set_text(text.split('\n'))
            self._ctx.set_filename('')

        # Create the Tokenizer, Parser and Interpreter instances
        tokenizer = Tokenizer(self._ctx)
        tokenizer.get_logger().setLevel(self.get_logger().level)
        parser = Parser(tokenizer, self._ctx)
        interpreter = Interpreter(self._ctx)
        interpreter.get_logger().setLevel(self.get_logger().level)

        # parse the input and create a AST
        tree = parser.parse()
        # interpret the AST and execute all statements contained within
        interpreter.interpret(tree)
        # result will hold the contents of the parsed template
        result = interpreter.get_parsed_template()

        if self._output_mode == TemplateParser.OUTPUTMODE_FILE:
            outfile = self._ctx.outputfile()

            if outfile == '':
                # Prompt for outputfile
                outfile = input('Please enter the filename of the new file: ')

            # replace variables in outputfile
            outfile = self._ctx.process_variables(outfile)
            path = os.path.realpath(outfile)

            overwrite = True
            if os.path.exists(path):
                overwrite = cli.prompt('A file with the name {0} already exists. Overwrite?'.format(outfile))

            if overwrite:
                with open(path, 'w') as f:
                    f.write('\n'.join(result))

                print(Fore.GREEN + '√' + Fore.RESET + ' File ' + Style.BRIGHT + '{0}'.format(os.path.basename(path)) +
                      Style.RESET_ALL + ' has been created')

        elif self._output_mode == self.OUTPUTMODE_CONSOLE:
            print('\n'.join(result))

        return result
