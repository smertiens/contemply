import re

# Tokens

STRING, INTEGER, LIST, OBJNAME, EOL = 'STRING', 'INTEGER', 'LIST', 'OBJNAME', 'EOL',
LPAR, RPAR, COMMA, LSQRBR, RSQRBR, ASSIGN = 'LPAR', 'RPAR', 'COMMA', 'LSQRBR', 'RSQRBR', 'ASSIGN'


class ParserException(Exception):
    pass


def pprint_tokens(tokens):
    out = ''

    for t in tokens:
        out += t.type() + (' -> ' if t.type() != EOL else '')

    print(out)


class Token:

    def __init__(self, ttype, val=''):
        self._type = ttype
        self._val = val

    def value(self):
        return self._val

    def type(self):
        return self._type

    def __str__(self):
        return 'Token: {0} ({1})'.format(self._type, self._val)

    def __repr__(self):
        return self.__str__()


class Function:

    def __init__(self, name, args):
        self._name = name
        self._args = args

    def __str__(self):
        return 'Function: {0} ({1})'.format(self._name, self._args)

    def __repr__(self):
        return self.__str__()


class List:

    def __init__(self, items):
        self._items = items

    def __str__(self):
        return 'List: {0}'.format(self._items)

    def __repr__(self):
        return self.__str__()


class VariableAssignment:

    def __init__(self, varname, value):
        self._varname = varname
        self._value = value

    def __str__(self):
        return 'Assignment: {0} = {1}'.format(self._varname, self._value)

    def __repr__(self):
        return self.__str__()

class TemplateParser:

    def __init__(self):
        self._pos = 0
        self._text = ''
        self._token = None

    def _parse(self, text):
        self._pos = 0
        self._token = None
        self._text = text

        while self._get_chr() is not None:
            token = self._get_next_token()

            if token.type() == OBJNAME:
                objname = token.value()
                token = self._get_next_token()

                if token.type() == LPAR:
                    # function
                    func = self._process_function(objname)
                    print(func)

                elif token.type() == ASSIGN:
                    # assignment
                    assig = self._process_assignment(objname)
                    print(assig)
                else:
                    raise ParserException("Unexpected token: " + token)

    def _get_chr(self):
        try:
            return self._text[self._pos]
        except IndexError:
            return None

    def _advance(self):
        self._pos += 1

    def _lookahead(self, size=1):
        return self._text[self._pos:size]

    def _skip_whitespace(self):
        while self._get_chr().isspace():
            self._advance()

    def _get_next_token(self):
        token = None

        self._skip_whitespace()

        if self._get_chr().isalpha():
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
            token = Token(ASSIGN, '=')
            self._advance()

        elif self._get_chr() is None:
            return Token(EOL)

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

        while self._get_chr() is not None and self._get_chr() != '"' and self._get_chr() != '"':
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

            if token.type() in [STRING, INTEGER]:
                args.append(token)
            elif token.type() == LSQRBR:
                lst = self._process_list()
                args.append(lst)
            else:
                raise ParserException("Unvalid function argument.")

            token = self._get_next_token()

        return Function(funcname, args)

    def _process_assignment(self, varname):
        token = self._get_next_token()

        if token.type() not in [STRING, INTEGER]:
            raise ParserException("Expected String or Integer")

        return VariableAssignment(varname, token)

    def _process_list(self):
        token = self._get_next_token()
        lst = []

        while token.type() != RSQRBR and token.type():
            if token.type() == COMMA:
                token = self._get_next_token()
                continue

            if token.type() in [STRING, INTEGER]:
                lst.append(token)
            elif token.type() == LSQRBR:
                lst = self._process_list()
                lst.append(lst)
            else:
                raise ParserException("Invalid list value.")

            token = self._get_next_token()

        return List(lst)

    def parseFile(self):
        pass
