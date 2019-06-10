#
# Contemply - A code generator that creates boilerplate files from templates
#
# Copyright (C) 2019  Sean Mertiens
# For more information on licensing see LICENSE file
#

import os, re, sys

import contemply.cli as cli
from colorama import Fore, Style
from contemply.interpreter import *
from contemply.tokenizer import *
from contemply.storage import get_secure_path


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
        self._line_pos = 0

    def set_text(self, text):
        """
        Sets the text for parsing

        :param str text: The string to parse
        :return:
        """
        self._text = text

    def text(self):
        """
        Returns the lines to parse

        :return: List with lines to parse
        """
        return self._text

    def set_filename(self, val):
        """
        Sets the path of the template file.

        :param str val: Path to a template file
        """
        self._filename = val

    def set_line(self, val):
        """
        Sets the current line. Should usually not be used.

        :param int val: line number
        """
        self._line = val

    def set_pos(self, val):
        """
        Sets the current position inside the text (column)

        :param int val: The current character position
        """
        diff =  val - self._pos
        self._pos = val
        self._line_pos = self._line_pos +  diff

    def set_line_pos(self, val):
        """
        Sets the current position inside the line (column)
        Only used for error messages

        :param int val: The current character position
        """
        self._line_pos = val

    def line_pos(self):
        """
        Gets the current position inside the line (column)
        Only used for error messages
        """
        return self._line_pos


    def filename(self):
        """
        Returns the current template file

        :return: Path to template file
        :rtype: str
        """
        return self._filename

    def line(self):
        """
        Returns the current line in the template file

        :return: Line  number
        :rtype: int
        """
        return self._line

    def pos(self):
        """
        Returns the current character position inside the template file line
        :return: Character position
        :rtype: int
        """
        return self._pos

    def set_outputfile(self, file):
        """
        Sets the path to the output file under which the rendered template is saved (can be set form within the
        template via setOutput())

        :param str file: Path to the file (can be relative to the current directory)
        """
        self._outputfile = file

    def outputfile(self):
        """
        Returns the path to the outputfile

        :return: Path to outputfile
        :rtype: str
        """
        return self._outputfile

    def set(self, varname, v):
        """
        Sets the value of a variable

        :param str varname: The name of the variable
        :param Any v: Variable value
        """
        self._data[varname] = v

    def get(self, varname):
        """
        Returns the value of a variable

        :param str varname: Name of the variable
        :return: Variable value
        :rtype: Any
        :raises: ParserError
        """
        try:
            return self._data[varname]
        except KeyError:
            raise ParserError('Unknown variable: {0}'.format(varname), self)

    def has(self, varname):
        """
        Checks whether a variable with the given name exists.

        :param str varname: Name of the variable
        :return: True if variable exists, False if not
        :rtype: bool
        """
        return varname in self._data

    def get_all(self):
        """
        Returns a dictionary with all the variables

        :return: A dictionary with all defined variables
        :rtype: dict
        """
        return self._data

    def set_position(self, line, col):
        """
        Sets the current position inside the template. Should not be used.

        :param int line: The new line
        :param int col: THe new column
        """
        self.set_line(line)
        self.set_pos(col)

    def process_variables(self, text):
        """
        Replaces variabels inside a string.
        The content line notation is used (variable names start with a $).
        Variable names and values are taken from this TemplateContexte instance.

        :param str text: The text to parse
        :return: The parsed text
        :rtype: str
        """

        def check_and_replace(match):
            varname = match.group(1)[1:]  # strip trailing $

            if not self.has(varname):
                raise ParserError('Unknown variable: "{0}"'.format(varname), self)
            else:
                val = self.get(varname)

                if isinstance(val, list) and match.group(2) is not None:
                    val = val[int(match.group(3))]
                if not isinstance(val, str):
                    val = str(val)

                return '{0}{1}'.format(val, match.group(4))

        p = re.compile(r'(\$[\w_]+)(\[(\d+)\])?(\s|\W|$)', re.MULTILINE)
        text = p.sub(check_and_replace, text)

        return text


class Parser:
    """
    This class will do the actual parsing. It needs a Tokenizer instance and will then create
    an AST from the input tokens that can be interpreted using the Interpreter.
    """

    def __init__(self, tokenizer, ctx):
        self._token = None
        self._tokenizer = tokenizer
        self._ctx = ctx

        self._cmd_block_mode = False

    def _raise_error(self, msg):
        raise ParserError(msg, self._ctx)

    def get_logger(self):
        return logging.getLogger(self.__module__)

    def parse(self):
        root = self._consume_template()
        return root

    def _consume_block(self, delim=(EOF,)):
        node = Block()

        self._token = Token(None)

        while self._token.type() not in delim:
            peek = self._tokenizer.get_next_token(True)

            if peek.type() == EOF and EOF not in delim:
                raise ParserError('Unexpected end of file, expected {}'.format(', '.join(delim)))

            if peek.type() == COMMENT:
                self._tokenizer.skip_until('\n')
                self._token = self._tokenizer.get_next_token()  # NEWLINE or EOF

            elif peek.type() == CMD_BLOCK:
                self._token = self._tokenizer.get_next_token()
                self._cmd_block_mode = not self._cmd_block_mode
                self._token = self._tokenizer.get_next_token()

            elif peek.type() == CMD_LINE_START or self._cmd_block_mode:
                if not self._cmd_block_mode:
                    self._token = self._tokenizer.get_next_token()
                    self._token = self._tokenizer.get_next_token()
                else:
                    self._token = self._tokenizer.get_next_token()

                # Check again for delim since block consumption is non-inclusive
                if self._token.type() in delim:
                    return node

                node.children.append(self._consume_cmd_line())
            else:
                node.children.append(self._consume_content_line())

            # all statements should consume until NEWLINE or end of file
            if self._token.type() not in (NEWLINE, EOF):
                raise InternalError('Statments did not consume whole line, got ' + self._token.type() + ' instead.',
                                    self._ctx)
            else:
                self._ctx.set_line(self._ctx.line() + 1)
                self._ctx.set_line_pos(0)

        return node

    def _consume_template(self):

        node = Template()

        self._ctx.set_position(0, 0)
        self._tokenizer.update_position()

        node.main_block = self._consume_block()

        return node

    def _consume_next_token(self, ttype):
        if self._token.type() == ttype:
            return self._tokenizer.get_next_token()
        else:
            raise ParserError('Unexpected token, got ' + self._token.type() + ' expected ' + ttype, self._ctx)

    def _consume_cmd_line(self):
        statement = self._consume_statement()
        return CommandLine(statement)

    def _consume_symbol(self):
        name = self._token.value()
        self._token = self._consume_next_token(SYMBOL)

        if self._token.type() == LPAR:
            node = self._consume_function(name)
        elif self._token.type() in (ASSIGN, ASSIGN_PLUS):
            node = self._consume_assignment(name)
        else:
            index = None
            if self._token.type() == LSQRBR:
                self._token = self._consume_next_token(LSQRBR)
                index = self._token.value()
                self._token = self._consume_next_token(INTEGER)
                self._token = self._consume_next_token(RSQRBR)

            node = Variable(name, index)

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
            raise ParserError('Unexpected token-type: ' + self._token.type(), self._ctx)
        return node

    def _consume_while_loop(self):
        self._token = self._consume_next_token(WHILE)
        expr = self._consume_expression()
        block = self._consume_block((ENDWHILE,))
        node = While(expr, block)
        self._token = self._consume_next_token(ENDWHILE)

        return node

    def _consume_for_loop(self):
        self._token = self._consume_next_token(FOR)
        itemvar = self._consume_symbol()
        self._token = self._consume_next_token(IN)
        listvar = self._consume_symbol()

        block = self._consume_block((ENDFOR,))
        node = For(listvar, itemvar, block)
        self._token = self._consume_next_token(ENDFOR)

        return node

    def _consume_statement(self):
        if self._token.type() == SYMBOL:
            node = self._consume_symbol()
        elif self._token.type() == IF:
            node = self._consume_if_block()
        elif self._token.type() == ELSEIF:
            return NoOp()
        elif self._token.type() == ELSE:
            return NoOp()
        elif self._token.type() == ENDIF:
            self._token = self._consume_next_token(ENDIF)
            return NoOp()
        elif self._token.type() == WHILE:
            node = self._consume_while_loop()
        elif self._token.type() == ENDWHILE:
            node = NoOp()
        elif self._token.type() == FOR:
            node = self._consume_for_loop()
        elif self._token.type() == ENDFOR:
            node = Endfor()
        elif self._token.type() == BREAK:
            self._token = self._consume_next_token(BREAK)
            node = Break()
        elif self._token.type() == FILE_BLOCK_START:
            node = self._consume_file_block_start()
        elif self._token.type() == FILE_BLOCK_END:
            self._token = self._consume_next_token(FILE_BLOCK_END)
            node = FileBlockEnd()
        elif self._token.type() == NEWLINE:
            node = NoOp()
        else:
            raise ParserError('Unknown block start: ' + self._token.type(), self._ctx)

        return node

    def _consume_file_block_start(self):
        self._token = self._consume_next_token(FILE_BLOCK_START)
        node = FileBlockStart(self._token.value())
        self._token = self._consume_next_token(STRING)

        if self._token.type() == COMMA:
            self._token = self._consume_next_token(COMMA)
            node.create_missing_folders = self._consume_symbol()

        return node

    def _consume_expression(self):

        if self._token.type() in (STRING, INTEGER):
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
            return lval

        if self._token.type() in (STRING, INTEGER):
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
        block = self._consume_block((ELSE, ENDIF, ELSEIF))
        node = IFBlock()
        node._if.append(If(cond, block))

        while self._token.type() != ENDIF:

            if self._token.type() == ELSEIF:
                self._token = self._consume_next_token(ELSEIF)
                cond = self._consume_expression()
                elseif_block = self._consume_block((ELSE, ELSEIF, ENDIF))
                node._if.append(If(cond, elseif_block))

            elif self._token.type() == ELSE:
                self._token = self._consume_next_token(ELSE)
                else_block = self._consume_block((ENDIF,))
                node._else = else_block

            else:
                raise ParserError('Expected ENDIF or ELSE.', self._ctx)

        self._token = self._consume_next_token(ENDIF)
        return node

    def _consume_content_line(self):
        line = self._tokenizer.get_raw('\n')
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
        """
        Returns the logger instance for the parser.
        This log level will also be used for the tokenizer and interpreter.

        :returns: Logger instance
        :rtype: logging.Logger
        """
        return logging.getLogger(self.__module__)

    def get_template_context(self):
        """
        Returns the current template context instance

        :return: The current template context
        :rtype: TemplateContext
        """
        return self._ctx

    def set_output_mode(self, mode):
        """
        Sets the parsers output mode. If set to "console", the parsed template is output to the
        console. Defaults to OUTPUTMODE_FILE.

        :param mode: TemplateParser.OUTPUTMODE_CONSOLE | TemplateParser.OUTPUTMODE_FILE
        """
        self._output_mode = mode

    def parse_file(self, filename):
        """
        Parses the given filename

        :param str filename: The path to a file to parse
        :return: A list containing the lines of the parsed template
        :rtype: list
        """
        self._ctx.set_filename(os.path.basename(filename))

        with open(filename, 'r') as f:
            lines = f.read()

        self._ctx.set_text(lines)

        return self.parse()

    def parse(self, text=None):
        """
        Parses the given text. If no text is set, the parser will parse the content of the current
        TemplateContext.

        :param str text: A text to parse
        :return: A list containing the lines of the parsed template
        :rtype: list
        """
        if text is not None:
            self._ctx.set_text(text)
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
            for target_file, content in result.items():
                if target_file == Interpreter.DEFAULT_TARGET:
                    # The default target will only be created if the content is not empty.
                    if len(content) == 0:
                        continue

                    # In case setOutput is used - will be deprecated in some future release
                    if self._ctx.outputfile() != '':
                        target_file = self._ctx.outputfile()
                    else:
                        # Prompt for outputfile
                        outfile = cli.user_input('Please enter the filename of the new file: ')
                        target_file = self._ctx.process_variables(outfile)

                path = get_secure_path(os.getcwd(), target_file)
                disp_path = target_file.replace(os.getcwd(), '')

                overwrite = True
                if os.path.exists(path):
                    overwrite = cli.prompt('A file with the name {0} already exists. Overwrite?'.format(disp_path))

                if overwrite:
                    with open(path, 'w') as f:
                        f.write('\n'.join(content))

                print(Fore.GREEN + '√' + Fore.RESET + ' File ' + Style.BRIGHT + '{0}'.format(disp_path) +
                      Style.RESET_ALL + ' has been created')

        elif self._output_mode == self.OUTPUTMODE_CONSOLE:
            for target_file, content in result.items():
                if target_file == Interpreter.DEFAULT_TARGET:
                    target_file = self._ctx.outputfile() if self._ctx.outputfile() != '' else '(No filename specified)'
                else:
                    target_file = target_file.replace(os.getcwd(), '')

                print(Fore.CYAN + target_file + ': ' + Fore.RESET)

                for line in content:
                    print('\t' + line)

        return result
