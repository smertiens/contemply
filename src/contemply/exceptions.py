#
# AtraxiCreator - GUI editor for AtraxiFlow scripts
#
# Copyright (C) 2019  Sean Mertiens
# For more information on licensing see LICENSE file
#

__all__ = ['TemplateException', 'ParserError', 'SyntaxError']


class TemplateException(Exception):

    def __init__(self, message, ctx=None):
        super().__init__(message)
        self.message = message
        self.ctx = ctx

    def __str__(self):
        if self.ctx is not None:
            line = self.ctx.text()[self.ctx.line()]
            marker = ''
            if line != '':
                marker = '{0}^'.format(' ' * self.ctx.pos())

            return '{6} in {1}, line {2}, col {3}: {0}\n{4}\n{5}'.format(self.message, self.ctx.filename(),
                                                                         self.ctx.line(), self.ctx.pos(),
                                                                         line, marker, self.__class__.__name__)
        else:
            return '{1}: {0}'.format(self.message, self.__class__.__name__)

    def __repr__(self):
        return self.__str__()


class ParserError(TemplateException):
    pass


class SyntaxError(TemplateException):
    pass
