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

    def __init__(self, name):
        self.name = name


class String(AST):

    def __init__(self, value):
        self.value = value


class Num(AST):

    def __init__(self, value):
        self.value = value


class Function(AST):

    def __init__(self, name, args):
        self.name = name
        self.args = args


class Assignment(AST):

    def __init__(self, variable, value):
        self.variable = variable
        self.value = value


class ArgumentList(AST):

    def __init__(self):
        self.children = []


class SimpleExpression(AST):

    def __init__(self, lval, op, rval):
        self.lval = lval
        self.op = op
        self.rval = rval


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