#
# Contemply - A code generator that creates boilerplate files from templates
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


class WhileLoop:

    def __init__(self, node, target_line):
        self.node = node

        # the line where the loop starts.
        self.target_line = target_line
        self.iterations = 0

    def increment_iterations(self):
        self.iterations += 1

    def __str__(self):
        return "While {0}".format(self.node.expr)

    def __repr__(self):
        return self.__str__()


class ForLoop:

    def __init__(self, node, target_line):
        self.node = node

        # the line where the loop starts.
        self.target_line = target_line
        self.iterations = 0

    def increment_iterations(self):
        self.iterations += 1

    def __str__(self):
        return "For {0} in {1}".format(self.node.itemvar, self.node.listvar)

    def __repr__(self):
        return self.__str__()


class Interpreter:
    MAX_LOOP_RUNS = 10  # 10000

    def __init__(self, ctx):
        self._BUILTINS = {
            'True': True,
            'False': False,
            'None': None
        }

        self._tree = []
        self._conditions = []
        self._loops = []
        self._skip_until = None
        self._ctx = ctx
        self._line = 0

        self._parsed_template = []

    def interpret(self, tree):
        self._tree = tree
        self.visit(tree)

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

    def _cleanup(self):
        if len(self._conditions) > 0:
            raise ParserError('There is still at least one open IF-block. Expected: ENDIF.', self._ctx)

        if len(self._loops) > 0:
            raise ParserError('There is still at least one open loop-block. Expected: ENDWHILE.', self._ctx)

        if self._skip_until is not None:
            raise ParserError('Unexpected end of template. Expected: {0}'.format(self._skip_until.__name__), self._ctx)

    ##########################
    # Internal functions
    ##########################

    def _internal_func_exit(self, args):
        if len(args) > 0:
            print(args[0])

        quit()

    def _internal_func__debugDumpStack(self, args):
        print(self._ctx.get_all())

    def _internal_func_break(self, args):
        if len(args) > 0:
            raise ParserError('break() taktes no arguments', self._ctx)

        try:
            active_loop = self._loops.pop()
        except IndexError:
            raise ParserError('Not in a loop.', self._ctx)

        if isinstance(active_loop, WhileLoop):
            self._skip_until = Endwhile
        elif isinstance(active_loop, ForLoop):
            self._skip_until = Endfor

    ##########################
    # Node visitors
    ##########################

    def visit(self, node):
        method_name = 'visit_' + type(node).__name__.lower()
        visitor = getattr(self, method_name, self.fallback_visit)
        # print('Visiting: '+type(node).__name__)
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
        self._line = 0

        while self._line < len(node.children):
            child = node.children[self._line]
            self.visit(child)

            self._line += 1

        self._cleanup()

    def visit_contentline(self, node):
        if self._skip_until is not None:
            # we can skip every contentline
            return

        if not self._skip_due_to_conditions():
            line = self._ctx.process_variables(node.content)
            self._parsed_template.append(line)

    def visit_commandline(self, node):
        if (self._skip_until is not None) and (not isinstance(node.statement, self._skip_until)) \
                and (not type(node.statement) in [Endif, Else, If]):
            # this makes sure that conditionals are seen, otherwise a ParserError would be raised
            # because there could be unclosed if-blocks remaining when using break() in a loop
            return
        elif self._skip_until is not None and isinstance(node.statement, self._skip_until):
            # we have reached the desired statement
            self._skip_until = None
            # skip this statement (skip_until means "including the given statement")
            return

        if type(node.statement) not in [Endif, Else]:
            if not self._skip_due_to_conditions():
                self.visit(node.statement)
        else:
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
        self._conditions.append(InterpeterCondition(self.visit(node.condition), InterpeterCondition.TYPE_IF))

    def visit_while(self, node):
        if self.visit(node.expr):
            self._loops.append(WhileLoop(node, self._line))
        else:
            # while condition not True -> skip next while block until ENDWHILE is discovered
            self._skip_until = Endwhile

    def visit_for(self, node):
        # Check listvar
        listvar = self.visit(node.listvar)

        if not isinstance(listvar, list):
            raise ParserError('Cannot iterate "{0}", expected a list.'.format(node.listvar.name), self._ctx)

        # No elements in list, no sense in running loop
        if len(listvar) == 0:
            self._skip_until = Endfor
            return

        # Initialize itemvar
        self._ctx.set(node.itemvar.name, listvar[0])
        self._loops.append(ForLoop(node, self._line))

        # Since we're now running the loop for the first time, we also need to increment the counter
        self._loops[-1].increment_iterations()

    def visit_endfor(self, node):
        # Get active loop
        try:
            active_loop = self._loops[-1]
        except IndexError:
            raise ParserError('Unexpected ENDFOR', self._ctx)

        # Check whether it's the loop we're looking for
        if not isinstance(active_loop, ForLoop):
            raise ParserError('Active loop is not a for loop.', self._ctx)

        # check if we're done with iterating
        listvar = self.visit(active_loop.node.listvar)
        if not active_loop.iterations < len(listvar):
            self._loops.pop()
        else:
            # set itemvar to new value
            self._ctx.set(active_loop.node.itemvar.name, listvar[active_loop.iterations])
            # jump to start of loop and run again from there
            self._line = active_loop.target_line
            active_loop.increment_iterations()

    def visit_endwhile(self, node):
        try:
            active_loop = self._loops[-1]
        except IndexError:
            raise ParserError('Unexpected ENDWHILE', self._ctx)

        if not isinstance(active_loop, WhileLoop):
            raise ParserError('Active loop is not a while loop.', self._ctx)

        if not self.visit(active_loop.node.expr):
            # the condition of the active loop does not match anymore so we can remove the loop from the stack
            self._loops.pop()
        else:
            if active_loop.iterations >= self.MAX_LOOP_RUNS:
                raise ParserError("Maximum loop iterations of {0} reached.".format(self.MAX_LOOP_RUNS))

            # jump back to the loop's start and increment the number of loop runs
            self._line = active_loop.target_line
            active_loop.increment_iterations()

    def visit_else(self, node):
        try:
            self._conditions.pop()
        except IndexError:
            raise ParserError("Unexpected ELSE", self._ctx)

        self._conditions.append(InterpeterCondition(self.visit(node.condition), InterpeterCondition.TYPE_ELSE))

    def visit_endif(self, node):
        try:
            self._conditions.pop()
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
