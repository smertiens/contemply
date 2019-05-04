# AtraxiCreator - GUI editor for AtraxiFlow scripts
#
# Copyright (C) 2019  Sean Mertiens
# For more information on licensing see LICENSE file
#

import contemply.functions
from contemply.exceptions import *
from contemply.ast import *


class InterpeterCondition:
    TYPE_IF, TYPE_ELSE, TYPE_ELSEIF = 'TYPE_IF', 'TYPE_ELSE', 'TYPE_ELSEIF'

    def __init__(self, expr, cond_type):
        self.expr = expr
        self.type = cond_type

    def __str__(self):
        return "Condition {0}, {1}".format(self.type, self.expr)

    def __repr__(self):
        return self.__str__()


class Interpreter:

    def __init__(self, ctx):
        self._BUILTINS = {
            'True': True,
            'False': False,
            'None': None
        }

        self._tree = []
        self._conditions = []
        self._ctx = ctx

        self._parsed_template = []

    def get_parsed_template(self):
        return self._parsed_template

    def _skip_due_to_conditions(self):
        result = False
        for cond in self._conditions:
            if (cond.type == InterpeterCondition.TYPE_IF and not cond.expr) or \
                    (cond.type == InterpeterCondition.TYPE_ELSE and cond.expr):
                result = True

        return result

    def visit(self, node):
        method_name = 'visit_' + type(node).__name__.lower()
        visitor = getattr(self, method_name, self.fallback_visit)
        return visitor(node)

    def fallback_visit(self, node):
        raise Exception('No visitor found for node {0}'.format(node))

    def visit_function(self, node):
        # function
        func = node.name
        args = self.visit(node.args)

        if hasattr(contemply.functions, '{0}'.format(func)):
            call = getattr(contemply.functions, '{0}'.format(func))
            call(args, self._ctx)
        else:
            raise ParserError("Unknown function: {0}".format(func), self._ctx)

    def visit_argumentlist(self, node):
        args = []
        for child in node.children:
            args.append(self.visit(child))
        return args

    def visit_num(self, node):
        return int(node.value)

    def visit_variable(self, node):
        if node.name in self._BUILTINS:
            return self._BUILTINS[node.name]

        if self._ctx.has(node.name):
            return self._ctx.get(node.name)
        else:
            raise ParserError('Unknown variable: "{0}"'.format(node.name), self._ctx)

    def visit_list(self, node):
        pylist = []

        for item in node.children:
            pylist.append(self.visit(item))

        return pylist

    def visit_template(self, node):
        for child in node.children:
            visit = True

            if visit:
                self.visit(child)

    def visit_contentline(self, node):
        if not self._skip_due_to_conditions():
            line = self._ctx.process_variables(node.content)
            self._parsed_template.append(line)

    def visit_commandline(self, node):
        if type(node.statement) not in [Endif, Else]:
            if not self._skip_due_to_conditions():
                self.visit(node.statement)
        else:
            self.visit(node.statement)

    def visit_assignment(self, node):
        self._ctx.set(node.variable, self.visit(node.value))

    def visit_string(self, node):
        return node.value

    def visit_if(self, node):
        self._conditions.append(InterpeterCondition(self.visit(node.condition), InterpeterCondition.TYPE_IF))

    def visit_else(self, node):
        try:
            active_cond = self._conditions.pop()
        except IndexError:
            ParserError("Unexpected ELSE", self._ctx)

        self._conditions.append(InterpeterCondition(self.visit(node.condition), InterpeterCondition.TYPE_ELSE))

    def visit_endif(self, node):
        try:
            active_cond = self._conditions.pop()
        except IndexError:
            ParserError("Unexpected ENDIF", self._ctx)

    def visit_simpleexpression(self, node):
        lval = self.visit(node.lval)
        rval = self.visit(node.rval)

        if node.op == '==':
            return lval == rval
        elif node.op == '<':
            return lval < rval
        elif node.op == '>':
            return lval > rval
        elif node.op == '<=':
            return lval <= rval
        elif node.op == '>=':
            return lval >= rval
        elif node.op == '!=':
            return lval != rval
        else:
            raise ParserError("Unrecognized operator: {0}".format(node.op))

    def visit_noop(self, node):
        pass

    def interpret(self, tree):
        self._tree = tree
        self.visit(tree)
