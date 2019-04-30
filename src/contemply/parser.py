#
# Contemply - A code generator that creates boilerplate files from templates
#
# Copyright (C) 2019  Sean Mertiens
# For more information on licensing see LICENSE file
#

import os, logging
import contemply.functions
from contemply.cpytypes import *


def pprint_tokens(tokens):
    out = ''

    for t in tokens:
        out += t.type() + (' -> ' if t.type() != EOL else '')

    print(out)


class TemplateContext:

    def __init__(self):
        self._data = {}
        self._outputfile = ''
        self._filename = ''
        self._line = 0
        self._pos = 0

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


class TemplateParser:
    VAR_PREFIX = '$'
    CMD_PREFIX = '#:'

    OUTPUTMODE_CONSOLE, OUTPUTMODE_FILE = 0, 1

    def __init__(self):
        self._pos = 0
        self._text = ''
        self._token = None
        self._cmd_stack = []
        self._block = None
        self._outputmode = self.OUTPUTMODE_FILE

    def get_logger(self):
        return logging.getLogger(self.__module__)

    def set_outputmode(self, mode):
        self._outputmode = mode

    def _process_variables(self):
        for k, v in self._ctx.get_all().items():
            if isinstance(v, str):
                self._text = self._text.replace('{1}{0}'.format(k, self.VAR_PREFIX), v)

    def _parse(self, text):
        """

        :param text: The line to parse
        :return:
        """
        self._pos = 0
        self._token = None
        self._text = text

        # check whether we should process this line

        if text.startswith(self.CMD_PREFIX):
            # Command
            self._text = self._text[2:]
        else:
            # Template code
            # check condition if any
            if self._block is not None:
                if self._block.type() == Block.IF_BLOCK and self._block.cond().solve() is False:
                    return ''
                elif self._block.type() == Block.ELSE_BLOCK and self._block.cond().solve() is True:
                    return ''

            # process variables only
            self._process_variables()
            return self._text

        # Interpret commands
        while self._get_chr() is not None:
            token = self._get_next_token()

            if token.type() == OBJNAME:
                objname = token.value()
                token = self._get_next_token()

                if token.type() == LPAR:
                    # function
                    func = self._process_function(objname)
                    if hasattr(contemply.functions, '{0}'.format(func.name())):
                        call = getattr(contemply.functions, '{0}'.format(func.name()))
                        call(func.args(), self._ctx)
                    else:
                        raise ParserException("Unknown function: {0}".format(func.name()))

                elif token.type() == ASSIGN:
                    # assignment
                    assig = self._process_assignment(objname)
                    self._ctx.set(assig.varname(), assig.value())

                else:
                    raise ParserException("Unexpected token: {0} in {1}".format(token, text))

            elif token.type() == IF:
                cond = self._process_if()
                self._block = Block(cond, Block.IF_BLOCK)

            elif token.type() == ENDIF:
                if self._block is None:
                    raise ParserException("Found ENDIF without preceding IF", self._ctx)

                self._block = None

            elif token.type() == ELSE:
                if self._block is None:
                    raise ParserException("Found ELSE without preceding IF")

                self._block.set_type(Block.ELSE_BLOCK)

        return ''

    def _get_chr(self):
        try:
            return self._text[self._pos]
        except IndexError:
            return None

    def _advance(self):
        self._pos += 1
        self._ctx.set_pos(self._pos)

    def _lookahead(self, size=1):
        return self._text[self._pos + 1:self._pos + 1 + size]

    def _skip_whitespace(self):
        while self._get_chr() is not None and self._get_chr().isspace():
            self._advance()

    def _get_next_token(self):
        token = None
        self._skip_whitespace()

        if self._get_chr() is None:
            return Token(EOL)

        if self._get_chr() == 'i' and self._lookahead() == 'f':
            token = Token(IF)
            self._advance()
            self._advance()

        elif self._get_chr() == 'e' and self._lookahead(3) == 'lse':
            token = Token(ELSE)

            for i in range(0, len('else')):
                self._advance()

        elif self._get_chr() == 'e' and self._lookahead(4) == 'ndif':
            token = Token(ENDIF)

            for i in range(0, len('endif')):
                self._advance()

        elif self._get_chr().isalpha():
            token = self._consume_objname()

        elif self._get_chr().isnumeric():
            token = self._consume_integer()

        elif self._get_chr() == '(':
            token = Token(LPAR, '(')
            self._advance()

        elif self._get_chr() == ')':
            token = Token(RPAR, '')
            self._advance()

        elif self._get_chr() == '[':
            token = Token(LSQRBR, '[')
            self._advance()

        elif self._get_chr() == ']':
            token = Token(RSQRBR, ']')
            self._advance()

        elif self._get_chr() == '"' or self._get_chr() == "'":
            self._advance()
            token = self._consume_string()

        elif self._get_chr() == ',':
            token = Token(COMMA, ',')
            self._advance()

        elif self._get_chr() == '=':
            if self._lookahead() == '=':
                token = Token(COMP_EQ, '==')
                self._advance()
            else:
                token = Token(ASSIGN, '=')

            self._advance()

        elif self._get_chr() == '<':
            if self._lookahead() == '=':
                token = Token(COMP_LT_EQ, '<=')
                self._advance()
            else:
                token = Token(COMP_LT, '<')

            self._advance()

        elif self._get_chr() == '>':
            if self._lookahead() == '=':
                token = Token(COMP_GT_EQ, '>=')
                self._advance()
            else:
                token = Token(COMP_GT, '>')

            self._advance()

        elif self._get_chr() == '!':
            if self._lookahead() == '=':
                token = Token(COMP_GT_EQ, '>=')
                self._advance()

            self._advance()

        else:
            raise ParserException("Unrecognized token at pos {0}".format(self._pos))

        return token

    #######################
    # Token consumption
    #######################

    def _consume_objname(self):
        objname = ''

        while self._get_chr() is not None and self._get_chr().isalpha() or self._get_chr().isnumeric():
            objname += self._get_chr()
            self._advance()

        return Token(OBJNAME, objname)

    def _consume_string(self):
        val = ''

        while self._get_chr() is not None and self._get_chr() != '"' and self._get_chr() != "'":
            val += self._get_chr()
            self._advance()

        self._advance()
        return Token(STRING, val)

    def _consume_integer(self):
        val = ''

        while self._get_chr() is not None and self._get_chr().isnumeric():
            val += self._get_chr()
            self._advance()

        return Token(INTEGER, int(val))

    #######################
    # Interpreter
    #######################

    def _process_function(self, funcname):
        token = self._get_next_token()
        args = []

        while token.type() != RPAR:
            if token.type() == EOL:
                raise ParserException("Unexpected EOL")

            if token.type() == COMMA:
                token = self._get_next_token()
                continue

            if token.type() in [STRING, INTEGER, OBJNAME]:
                args.append(token.value())
            elif token.type() == LSQRBR:
                lst = self._process_list()
                args.append(lst)
            else:
                raise ParserException("Invalid function argument.")

            token = self._get_next_token()

        return Function(funcname, args)

    def _process_assignment(self, varname):
        token = self._get_next_token()

        if token.type() not in [STRING, INTEGER]:
            raise ParserException("Expected String or Integer")

        return VariableAssignment(varname, token.value())

    def _process_list(self):
        token = self._get_next_token()
        lst = []

        while token.type() != RSQRBR and token.type():
            if token.type() == COMMA:
                token = self._get_next_token()
                continue

            if token.type() in [STRING, INTEGER]:
                lst.append(token.value())
            elif token.type() == LSQRBR:
                lst = self._process_list()
                lst.append(lst)
            else:
                raise ParserException("Invalid list value.")

            token = self._get_next_token()

        return lst

    def _resolve_objectname(self, objname):
        self.reserved_solution = {
            'True': True,
            'False': False,
            'None': None
        }

        if objname in self.reserved_solution:
            return self.reserved_solution[objname]

        # check for variable
        if self._ctx.has(objname):
            return self._ctx.get(objname)
        else:
            raise ParserException("Variable {0} not found".format(objname), self._ctx)

    def _convert_token_to_primitive_type(self, token):
        if token.type() == STRING or token.type() in OPERATORS:
            return str(token.value())

        elif token.type() == INTEGER:
            return int(token.value())

        elif token.type() == OBJNAME:
            return self._resolve_objectname(token.value())

    def _process_if(self):
        token = self._get_next_token()
        condition = None

        if token.type() not in [STRING, INTEGER, OBJNAME]:
            raise ParserException("Invalid LVAL for condition")

        lval = self._convert_token_to_primitive_type(token)

        token = self._get_next_token()
        if token.type() not in OPERATORS:
            raise ParserException("Expected operator")
        op = self._convert_token_to_primitive_type(token)

        token = self._get_next_token()
        if token.type() not in [STRING, INTEGER, OBJNAME]:
            raise ParserException("Invalid RVAL for condition")
        rval = self._convert_token_to_primitive_type(token)

        condition = Condition(lval, rval, op)
        return condition

    def _run(self):

        for cmd in self._cmd_stack:
            if isinstance(cmd, VariableAssignment):
                # TODO maybe NOTICE on overwrite
                self._ctx.set(cmd.varname(), cmd.value())

            elif isinstance(cmd, Function):
                if hasattr(contemply.functions, 'func_{0}'.format(cmd.name())):
                    func = getattr(contemply.functions, 'func_{0}'.format(cmd.name()))
                    func(cmd.args(), self._ctx)
                else:
                    raise ParserException("Unknown function: {0}".format(cmd.name()))

    def parse_file(self, filename):

        self._ctx = TemplateContext()
        self._ctx.set_filename(os.path.basename(filename))
        lines = []
        self._cmd_stack = []

        with open(filename, 'r') as f:
            for line in f:
                lines.append(line)

        # assemble output
        output = []
        for lineno, line in enumerate(lines):
            self._ctx.set_line(lineno + 1)
            line = self._parse(line)
            output.append(line)

        if self._outputmode == TemplateParser.OUTPUTMODE_FILE:
            outfile = self._ctx.outputfile()
            if outfile == '':
                # Prompt for outputfile
                outfile = input('Please enter the filename of the new file: ')

            # replace variables in outputfile
            for k, v in self._ctx.get_all().items():
                if isinstance(v, str):
                    outfile = outfile.replace('{1}{0}'.format(k, TemplateParser.VAR_PREFIX), v)

            path = os.path.realpath(outfile)

            with open(path, 'w') as f:
                f.write(''.join(output))

        elif self._outputmode == self.OUTPUTMODE_CONSOLE:
            print(''.join(output))

    def parse(self, text):
        self._ctx = TemplateContext()
        return self._parse(text)
