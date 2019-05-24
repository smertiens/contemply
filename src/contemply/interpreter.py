#
# Contemply - A code generator that creates boilerplate files from templates
#
# Copyright (C) 2019  Sean Mertiens
# For more information on licensing see LICENSE file
#

import logging
import sys

import contemply.functions
from contemply.ast import *
from contemply.exceptions import *


class Interpreter:
    MAX_LOOP_RUNS = 10000

    def __init__(self, ctx):
        self._BUILTINS = {
            'True': True,
            'False': False,
            'None': None
        }

        self._tree = []
        self._ctx = ctx
        self._line = 0

        self._break_current_loop = None
        self._loops_running = 0

        self._parsed_template = []

    def interpret(self, tree):
        self._tree = tree
        self.visit(tree)

    def get_logger(self):
        return logging.getLogger(self.__module__)

    def get_parsed_template(self):
        return self._parsed_template

    def _cleanup(self):
        pass

    ##########################
    # Internal functions
    ##########################

    def _internal_func_exit(self, args):
        if len(args) > 0:
            print(args[0])

        sys.exit()

    def _internal_func__debugDumpStack(self, args):
        print(self._ctx.get_all())

    ##########################
    # Node visitors
    ##########################

    def visit(self, node):
        method_name = 'visit_' + type(node).__name__.lower()
        visitor = getattr(self, method_name, self.fallback_visit)
        # print('Visiting: ' + type(node).__name__)
        return visitor(node)

    def fallback_visit(self, node):
        raise ParserError('No visitor found for node {0}'.format(node))

    def visit_function(self, node):
        # function
        func = node.name
        args = self.visit(node.args)

        # check for internal function
        if hasattr(self, '_internal_func_{0}'.format(func)):
            call = getattr(self, '_internal_func_{0}'.format(func))
            return call(args)

        if hasattr(contemply.functions, '{0}'.format(func)):
            call = getattr(contemply.functions, '{0}'.format(func))
            return call(args, self._ctx)
        else:
            raise ParserError("Unknown function: {0}".format(func), self._ctx)

    def visit_break(self, node):
        if self._loops_running <= 0:
            raise ParserError("Unexpected BREAK: no surrounding loop found", self._ctx)

        self._break_current_loop = True

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
            var = self._ctx.get(node.name)
            if node.index is not None:
                if isinstance(var, list):
                    return var[node.index]
                else:
                    raise ParserError('Variable "{0}" is not a list.'.format(node.name), self._ctx)
            else:
                return var
        else:
            raise ParserError('Unknown variable: "{0}"'.format(node.name), self._ctx)

    def visit_list(self, node):
        pylist = []

        for item in node.children:
            pylist.append(self.visit(item))

        return pylist

    def visit_template(self, node):
        self.visit(node.main_block)

    def visit_block(self, node):
        for item in node.children:
            self.visit(item)

            if self._break_current_loop is True:
                # Do not process any more statements from this block
                break

    def visit_contentline(self, node):
        line = self._ctx.process_variables(node.content)
        self._parsed_template.append(line)

    def visit_commandline(self, node):
        self.visit(node.statement)

    def visit_assignment(self, node):
        if node.type == 'ASSIGN':
            self._ctx.set(node.variable, self.visit(node.value))
        elif node.type == 'ASSIGN_PLUS':
            list_var = self._ctx.get(node.variable)

            # check var type
            if not isinstance(list_var, list):
                raise ParserError("Expected variable of type 'list'.", self._ctx)
            else:
                list_var.append(self.visit(node.value))

    def visit_string(self, node):
        return node.value

    def visit_if(self, node):
        if self.visit(node.condition):
            self.visit(node.block)
            return True
        else:
            return False

    def visit_ifblock(self, node):
        results = []
        for item in node._if:
            results.append(self.visit(item))

        if True not in results and node._else is not None:
            # all conditions returned false -> execute else block
            self.visit(node._else)

    def visit_while(self, node):
        counter = 0
        self._loops_running += 1

        while (self.visit(node.expr)):
            if counter >= self.MAX_LOOP_RUNS:
                raise ParserError("Maximum loop iterations of {0} reached.".format(self.MAX_LOOP_RUNS))
            self.visit(node.block)

            if self._break_current_loop:
                self._break_current_loop = False
                break

            counter += 1

        self._loops_running -= 1

    def visit_for(self, node):
        # Check listvar
        listvar = self.visit(node.listvar)

        if not isinstance(listvar, list):
            raise ParserError('Cannot iterate "{0}", expected a list.'.format(node.listvar.name), self._ctx)

        # No elements in list, no sense in running loop
        if len(listvar) == 0:
            return

        self._loops_running += 1

        for item in listvar:
            if self._break_current_loop:
                self._break_current_loop = False
                break

            self._ctx.set(node.itemvar.name, item)
            self.visit(node.block)

        self._loops_running -= 1

    def visit_else(self, node):
        pass

    def visit_endif(self, node):
        pass

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
