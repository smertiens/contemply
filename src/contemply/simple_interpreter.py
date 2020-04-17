import contemply.simple_ast as AST
from contemply import cli

class InterpreterException(Exception):
    pass


class TemplateContext:

    def __init__(self):
        self.filename = None
        self.content = []

class Interpreter:

    def get_logger(self):
        """
        Returns the logger instance for the parser.
        This log level will also be used for the tokenizer and interpreter.

        :returns: Logger instance
        :rtype: logging.Logger
        """
        return logging.getLogger(self.__module__)

    def raise_exception(self, msg):
        raise InterpreterException('{} in {} on line {}'.format(msg, 'x', self.pos + 1))

    def __init__(self):
        
        self.call_stack = []
        self.symbol_table = {}
        self.pos = 0

        self.allowed_internals = {
            'Output': {
                'allowed': ['@console', '*'],
            },
        }

        self.internals = {}
        self.template_ctx = None

    def set_symbol_value(self, symbol, val):
        self.symbol_table[symbol] =  val

    def advance_pos(self):
        self.pos += 1

    def set_pos (self, pos):
        self.pos = pos

    def run(self, parse_tree):

        while (self.pos < len(parse_tree)):
            token = parse_tree[self.pos]
            self.visit(token)
            self.advance_pos() 

    def visit(self, node):
        method_name = 'visit_' + type(node).__name__.lower()
        visitor = getattr(self, method_name, self.fallback_visit)
        return visitor(node)

    def fallback_visit(self, node):
        self.raise_exception('No visitor found for node {0}'.format(node))

    def visit_sectionstart(self, node):
        self.template_ctx = TemplateContext()

    def visit_sectionend(self, node):
        pass

    def visit_null(self, node):
        pass

    def visit_internalassignment(self, node: AST.InternalAssignment):
        if not node.varname in self.allowed_internals:
            self.raise_exception('Unknown internal value {}'.format(node.varname))
        
        if (not node.value in self.allowed_internals[node.varname]['allowed']) and \
            '*' not in self.allowed_internals[node.varname]['allowed']:
            self.raise_exception('Invalid value "{}" for internal setting {}'.format(node.value, node.varname))

        self.internals[node.varname] = node.value 

    def visit_assignment(self, node: AST.Assignment):
        self.set_symbol_value(node.varname, node.value)

    def visit_prompt(self, node: AST.Prompt):
        self.set_symbol_value(node.target_var, cli.user_input(node.text))

    def visit_collectionloop(self, node: AST.CollectionLoop):
        self.set_symbol_value(node.target_var, cli.collect(node.text))

    def visit_optionlist(self, node: AST.Optionlist):
        self.set_symbol_value(node.target_var, cli.choose(node.text, node.options))

    def visit_content(self, node: AST.Content):
        self.template_ctx.content.append(node.line)