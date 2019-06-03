#
# Contemply - A code generator that creates boilerplate files from templates
#
# Copyright (C) 2019  Sean Mertiens
# For more information on licensing see LICENSE file
#

import logging

from contemply.exceptions import *

# Tokens
STRING, INTEGER, LIST, SYMBOL, EOF = 'STRING', 'INTEGER', 'LIST', 'SYMBOL', 'EOF',
LPAR, RPAR, COMMA, LSQRBR, RSQRBR, ASSIGN, ASSIGN_PLUS, NEWLINE = 'LPAR', 'RPAR', 'COMMA', 'LSQRBR', 'RSQRBR', 'ASSIGN', 'ASSIGN_PLUS', 'NEWLINE'
IF, ELSE, ENDIF, WHILE, ENDWHILE, FOR, IN, ENDFOR, ELSEIF, BREAK = 'IF', 'ELSE', 'ENDIF', 'WHILE', 'ENDWHILE', 'FOR', 'IN', 'ENDFOR', 'ELSEIF', 'BREAK'

OPERATORS = COMP_EQ, COMP_LT, COMP_GT, COMP_LT_EQ, COMP_GT_EQ, COMP_NOT_EQ, ADD, SUB, DIV, MULT = 'COMP_EQ', 'COMP_LT', 'COMP_GT', 'COMP_LT_EQ', \
                                                                                                  'COMP_GT_EQ', 'COMP_NOT_EQ', 'ADD', 'SUB', 'DIV', 'MULT'
CMD_LINE_START, COMMENT, CMD_BLOCK = 'CMD_LINE_START', 'COMMENT', 'CMD_BLOCK'
RESERVED = 'True', 'False', 'None', 'for', 'in', 'while', 'endwhile', 'endif', 'if', 'else', 'endfor', 'elseif', 'endif', 'break'


class Token:

    def __init__(self, ttype, val=None):
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


class Tokenizer:
    def __init__(self, ctx):
        self._pos = 0
        self._line = 0
        self._token = None
        self._ctx = ctx
        self._text = ''

        self.update_position()

    def get_logger(self):
        return logging.getLogger(self.__module__)

    def find_all(self):
        token = self.get_next_token()
        lst = []
        while token.type() != EOF:
            lst.append(token)
            token = self.get_next_token()

        return lst

    def update_position(self):
        self._line = self._ctx.line()
        self._text = self._ctx.text()  # [self._line]
        self._pos = self._ctx.pos()

    def set_text(self, text):
        self._text = text

    def get_chr(self):
        try:
            return self._text[self._pos]
        except IndexError:
            return None

    def _advance(self):
        self._pos += 1
        self._ctx.set_pos(self._pos)

    def lookahead(self, size=1):
        try:
            return self._text[self._pos + 1:self._pos + 1 + size]
        except IndexError:
            return None

    def _skip_whitespace(self):
        while self.get_chr() is not None and self.get_chr().isspace() and self.get_chr() != '\n':
            self._advance()

    def get_raw(self, end_delim='\n'):

        raw = ''
        while self.get_chr() is not None and self.get_chr() != end_delim:
            raw += self.get_chr()
            self._advance()

        return raw

    def skip_until(self, delim='\n'):
        while self.get_chr() is not None and self.get_chr() not in delim:
            self._advance()

    def get_next_token(self, peek=False):
        """
        Retrieves the next token from the text stream.
        The peek option is ONLY to be used to determine the start of the line so content lines can be consumed
        without having them tokenized/stripped of whitespace before.

        :param bool peek: If TRUE, the tokenizer will not advance. In case the token length is undetermined (e.g.
                            strings, integer, symbols, ...) only an empty token of the corresponding type is returned.
        :return: The next token
        :rtype: Token
        """
        token = None
        advance = 0

        if not peek:
            self._skip_whitespace()

        if self.get_chr() is None:
            return Token(EOF)

        if self.get_chr() == 'i' and self.lookahead() == 'f':
            token = Token(IF)
            advance = 2

        elif self.get_chr() == 'e' and self.lookahead(4) == 'ndif':
            token = Token(ENDIF)
            advance = len('endif')

        elif self.get_chr() == 'e' and self.lookahead(7) == 'ndwhile':
            token = Token(ENDWHILE)
            advance = len('endwhile')

        elif self.get_chr() == 'e' and self.lookahead(5) == 'ndfor':
            token = Token(ENDFOR)
            advance = len('endfor')

        elif self.get_chr() == 'e' and self.lookahead(5) == 'lseif':
            token = Token(ELSEIF)
            advance = len('elseif')

        elif self.get_chr() == 'e' and self.lookahead(3) == 'lse':
            token = Token(ELSE)
            advance = len('else')

        elif self.get_chr() == 'w' and self.lookahead(4) == 'hile':
            token = Token(WHILE)
            advance = len('while')

        elif self.get_chr() == 'f' and self.lookahead(2) == 'or':
            token = Token(FOR)
            advance = 3

        elif self.get_chr() == 'i' and self.lookahead(2) == 'n ':
            token = Token(IN)
            advance = 2

        elif self.get_chr() == 'b' and self.lookahead(4) == 'reak':
            token = Token(BREAK)
            advance = 5

        elif self.get_chr().isalpha() or self.get_chr() == '_':
            if peek:
                token = Token(SYMBOL)
            else:
                token = self._consume_symbol()

        elif self.get_chr().isnumeric():
            if peek:
                token = Token(INTEGER)
            else:
                token = self._consume_integer()

        elif self.get_chr() == '#' and self.lookahead(2) == '::':
            token = Token(CMD_BLOCK)
            advance = 3

        elif self.get_chr() == '#' and self.lookahead() == ':':
            token = Token(CMD_LINE_START)
            advance = 2

        elif self.get_chr() == '#' and self.lookahead() == '%':
            token = Token(COMMENT)
            advance = 2

        elif self.get_chr() == '\n':
            token = Token(NEWLINE)
            advance = 1

        elif self.get_chr() == '(':
            token = Token(LPAR, '(')
            advance = 1

        elif self.get_chr() == ')':
            token = Token(RPAR, '')
            advance = 1

        elif self.get_chr() == '[':
            token = Token(LSQRBR, '[')
            advance = 1

        elif self.get_chr() == ']':
            token = Token(RSQRBR, ']')
            advance = 1

        elif self.get_chr() == '"':
            # Peek is not available for strings so we return an empty string token
            if peek:
                token = Token(STRING)
            else:
                self._advance()
                token = self._consume_string('"')

        elif self.get_chr() == "'":
            # Peek is not available for strings so we return an empty string token
            if peek:
                token = Token(STRING)
            else:
                self._advance()
                token = self._consume_string("'")

        elif self.get_chr() == ',':
            token = Token(COMMA, ',')
            advance = 1

        elif self.get_chr() == '+' and self.lookahead() == '=':
            token = Token(ASSIGN_PLUS, '+=')
            advance = 2

        elif self.get_chr() == '+':
            token = Token(ADD, '+')
            advance = 1

        elif self.get_chr() == '-':
            token = Token(ADD, '-')
            advance = 1

        elif self.get_chr() == '/':
            token = Token(DIV, '/')
            advance = 1

        elif self.get_chr() == '*':
            token = Token(MULT, '*')
            advance = 1

        elif self.get_chr() == '=':
            if self.lookahead() == '=':
                token = Token(COMP_EQ, '==')
                advance = 2
            else:
                token = Token(ASSIGN, '=')
                advance = 1

        elif self.get_chr() == '<':
            if self.lookahead() == '=':
                token = Token(COMP_LT_EQ, '<=')
                advance = 2
            else:
                token = Token(COMP_LT, '<')
                advance = 1

        elif self.get_chr() == '>':
            if self.lookahead() == '=':
                token = Token(COMP_GT_EQ, '>=')
                advance = 2
            else:
                token = Token(COMP_GT, '>')
                advance = 2

        elif self.get_chr() == '!':
            if self.lookahead() == '=':
                token = Token(COMP_NOT_EQ, '!=')
                advance = 2
            else:
                advance = 1

        else:
            if peek:
                # Peek can also look at a contentline at the moment, so some tokens might not be recognized
                # this should result in a token of uknown type
                return Token(None)
            else:
                raise SyntaxError("Unrecognized token '{0}'".format(self.get_chr()), self._ctx)

        if not peek:
            for i in range(0, advance):
                self._advance()

        return token

    def _consume_symbol(self):
        name = ''

        while (self.get_chr() is not None) and (
                self.get_chr().isalpha() or self.get_chr().isnumeric() or self.get_chr() == '_'):
            name += self.get_chr()
            self._advance()

        return Token(SYMBOL, name)

    def _consume_string(self, delim):
        val = ''

        while self.get_chr() != delim:
            if self.get_chr() == '\n' or self.get_chr() is None:
                raise SyntaxError('Unterminated string', self._ctx)

            val += self.get_chr()
            self._advance()

        self._advance()
        return Token(STRING, val)

    def _consume_integer(self):
        val = ''

        while self.get_chr() is not None and self.get_chr().isnumeric():
            val += self.get_chr()
            self._advance()

        return Token(INTEGER, int(val))
