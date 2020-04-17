#
# Contemply - A code generator that creates boilerplate files from templates
#
# Copyright (C) 2019-2020  Sean Mertiens
# For more information on licensing see LICENSE file
#

class SimpleAST:
    pass

class Null(SimpleAST):
    pass

class SectionStart(SimpleAST):
    pass

class SectionEnd(SimpleAST):
    pass

class Value(SimpleAST):
    def __init__(self, value):
        self.value = value

class Prompt(SimpleAST):
    def __init__(self, text, target_var):
        self.text = text
        self.target_var = target_var

class Echo(SimpleAST):
    def __init__(self, text):
        self.text = text

class Optionlist(SimpleAST):
    def __init__(self, text, options, target_var):
        self.text = text
        self.options = options
        self.target_var = target_var

class CollectionLoop(SimpleAST):
    def __init__(self, text, target_var):
        self.text = text
        self.target_var = target_var

class Assignment(SimpleAST):
    def __init__(self, varname, value):
        self.varname = varname
        self.value = value

class InternalAssignment(SimpleAST):
    def __init__(self, varname, value):
        self.varname = varname
        self.value = value

class SimpleExpression:

    def __init__(self, left, op, right):
        self.left = left
        self.operator = op
        self.right = right

class Content(SimpleAST):

    def __init__(self, line):
        self.line = line

class If(SimpleAST):

    def __init__(self, condition):
        self.condition = condition

class If(SimpleAST):

    def __init__(self, condition):
        self.condition = condition

class ElseIf(SimpleAST):

    def __init__(self, condition):
        self.condition = condition

class Else(SimpleAST):
    pass

class Endif(SimpleAST):
    pass

class For(SimpleAST):
    def __init__(self, condition):
        self.condition = condition

class EndFor(SimpleAST):
    pass
