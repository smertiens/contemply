#
# Contemply - A code generator that creates boilerplate files from templates
#
# Copyright (C) 2019  Sean Mertiens
# For more information on licensing see LICENSE file
#

class AST:
    pass


class Template(AST):

    def __init__(self):
        self.children = []


class Variable(AST):

    def __init__(self, name, index=None):
        self.name = name
        self.index = index

    def __str__(self):
        return '{0}'.format(self.name)

    def __repr__(self):
        return self.__str__()


class String(AST):

    def __init__(self, value):
        self.value = value


class Num(AST):

    def __init__(self, value):
        self.value = value

    def __str__(self):
        return '{0}'.format(self.value)

    def __repr__(self):
        return self.__str__()


class Function(AST):

    def __init__(self, name, args):
        self.name = name
        self.args = args


class Assignment(AST):

    def __init__(self, variable, value, assign_type='ASSIGN'):
        self.variable = variable
        self.value = value
        self.type = assign_type


class ArgumentList(AST):

    def __init__(self):
        self.children = []


class SimpleExpression(AST):

    def __init__(self, lval, op, rval):
        self.lval = lval
        self.op = op
        self.rval = rval

    def __str__(self):
        return '{0} {1} {2}'.format(self.lval, self.op, self.rval)

    def __repr__(self):
        return self.__str__()


class ContentLine(AST):

    def __init__(self, content):
        self.content = content


class CommandLine(AST):

    def __init__(self, statement):
        self.statement = statement


class If(AST):

    def __init__(self, condition):
        self.condition = condition


class Else(AST):

    def __init__(self, condition):
        self.condition = condition


class List(AST):

    def __init__(self):
        self.children = []


class NoOp(AST):
    pass


class Endif(AST):
    pass


class While(AST):

    def __init__(self, expr):
        self.expr = expr


class Endwhile(AST):
    pass


class For(AST):

    def __init__(self, listvar, itemvar):
        self.listvar = listvar
        self.itemvar = itemvar


class Endfor(AST):
    pass
