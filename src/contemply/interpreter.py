# AtraxiCreator - GUI editor for AtraxiFlow scripts
#
# Copyright (C) 2019  Sean Mertiens
# For more information on licensing see LICENSE file
#

import contemply.functions
from contemply.ast import *
from contemply.exceptions import *
import logging


class InterpeterCondition:
    TYPE_IF, TYPE_ELSE, TYPE_ELSEIF = 'TYPE_IF', 'TYPE_ELSE', 'TYPE_ELSEIF'

    def __init__(self, expr, cond_type):
        self.expr = expr
        self.type = cond_type

    def __str__(self):
        return "Condition {0}, {1}".format(self.type, self.expr)

    def __repr__(self):
        return self.__str__()


class InterpreterLoop:
    TYPE_WHILE = 'TYPE_WHILE'

    def __init__(self, node, ltype, target_line):
        self.node = node
        self.type = ltype
        self.target_line = target_line
        self.iterations = 0

    def increment_iterations(self):
        self.iterations += 1

    def __str__(self):
        return "Condition {0}, {1}".format(self.type, self.node.expr)

    def __repr__(self):
        return self.__str__()


class Interpreter:
    MAX_LOOP_RUNS = 10000

    def __init__(self, ctx):
        self._BUILTINS = {
            'True': True,
            'False': False,
            'None': None
        }

        self._tree = []
        self._conditions = []
        self._loops = []
        self._ctx = ctx
        self._line = 0

        self._parsed_template = []

    def get_logger(self):
        return logging.getLogger(self.__module__)

    def get_parsed_template(self):
        return self._parsed_template

    def _skip_due_to_conditions(self):
        result = False
        for cond in self._conditions:
            if (cond.type == InterpeterCondition.TYPE_IF and not cond.expr) or \
                    (cond.type == InterpeterCondition.TYPE_ELSE and cond.expr):
                result = True

        return result

    def _get_active_loop(self):
        try:
            return self._loops[-1]
        except IndexError:
            return None

    def visit(self, node):
        method_name = 'visit_' + type(node).__name__.lower()
        visitor = getattr(self, method_name, self.fallback_visit)
        # print('Visiting: '+type(node).__name__)
        return visitor(node)

    def fallback_visit(self, node):
        raise Exception('No visitor found for node {0}'.format(node))

    def visit_function(self, node):
        # function
        func = node.name
        args = self.visit(node.args)

        if hasattr(contemply.functions, '{0}'.format(func)):
            call = getattr(contemply.functions, '{0}'.format(func))
            return call(args, self._ctx)
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
        self._line = 0

        while self._line < len(node.children):
            child = node.children[self._line]
            self.visit(child)

            self._line += 1

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

    def visit_while(self, node):
        if self.visit(node.expr):
            self._loops.append(InterpreterLoop(node, InterpreterLoop.TYPE_WHILE, self._line))

    def visit_endwhile(self, node):
        try:
            active_loop = self._loops[-1]
        except IndexError:
            raise ParserError('Unexpected ENDWHILE', self._ctx)

        if not self.visit(active_loop.node.expr):
            self._loops.pop()
        else:
            if active_loop.iterations >= self.MAX_LOOP_RUNS:
                raise ParserError("Maximum loop iterations of {0} reached.".format(self.MAX_LOOP_RUNS))

            self._line = active_loop.target_line
            active_loop.increment_iterations()

    def visit_else(self, node):
        try:
            active_cond = self._conditions.pop()
        except IndexError:
            raise ParserError("Unexpected ELSE", self._ctx)

        self._conditions.append(InterpeterCondition(self.visit(node.condition), InterpeterCondition.TYPE_ELSE))

    def visit_endif(self, node):
        try:
            active_cond = self._conditions.pop()
        except IndexError:
            raise ParserError("Unexpected ENDIF", self._ctx)

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
        elif node.op == '+':
            return lval + rval
        elif node.op == '-':
            return lval - rval
        elif node.op == '/':
            return lval / rval
        elif node.op == '*':
            return lval * rval
        else:
            raise ParserError("Unrecognized operator: {0}".format(node.op), self._ctx)

    def visit_noop(self, node):
        pass

    def interpret(self, tree):
        self._tree = tree
        self.visit(tree)
