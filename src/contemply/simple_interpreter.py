import contemply.simple_ast as AST
from contemply.templates import TemplateContext
from contemply import cli
from contemply import builtin_functions
import re

class InterpreterException(Exception):
    pass

class BlockStackEmptyException(Exception):
    pass

class Stack:

    def __init__(self):
        self._data = []

    def push(self, elem):
        self._data.insert(0, elem)

    def update_first(self, data):
        self._data[0] = data

    def pop(self):
        self._data.pop(0)

    def get_first(self):
        if len(self._data) == 0:
            raise BlockStackEmptyException()

        return self._data[0]

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
        raise InterpreterException('{}'.format(msg))

    def __init__(self):

        self.string_re = re.compile(r'^(?:\"([^\"]*)\")|(?:\'([^\']*)\')$')

        self.block_stack = Stack()
        self.symbol_table = {}
        self.pos = 0

        self.allowed_internals = {
            'Output': {
                'allowed': ['@console', '@file'],
            },
            'StartMarker': {
                'allowed': ['*'],
            },
            'EndMarker': {
                'allowed': ['*'],
            },
            'Filename': {
                'allowed': ['*'],
            },
        }

        self.internals = {
            'StartMarker': '§',
            'EndMarker': '§',
        }

        self.builtins = {
            'true': True,
            'false': False
        }

        self._function_lookup = [builtin_functions]

        self.template_ctx = None

    def set_symbol_value(self, symbol, val):
        self.symbol_table[symbol] =  val

    def get_symbol_value(self, symbol):
        if symbol in self.symbol_table:
            return self.symbol_table[symbol]
        else:
            self.raise_exception('Variable "{}" not found'.format(symbol))

    def advance_pos(self):
        self.pos += 1

    def set_pos (self, pos):
        self.pos = pos

    def run(self, parse_tree):

        while self.pos < len(parse_tree):

            token = parse_tree[self.pos]
            
            if  not type(token) in (AST.Else, AST.Endif, AST.ElseIf):
            #if  not isinstance(token, AST.Else) and not isinstance(token, AST.Endif):
                try:
                    elem = self.block_stack.get_first()

                    if (elem['type'] == 'if'):
                        if not elem['condition']:
                            # if condition not met, skip lines
                            self.advance_pos()
                            continue

                except BlockStackEmptyException:
                    pass

            self.visit(token)
            self.advance_pos() 

        # save template context
        if self.template_ctx is not None:
            self.template_ctx.flush()

    def process_string(self, text: str):
        """
        Replaces variabels inside a string.
        The content line notation is used (variable names start with a $).
        Variable names and values are taken from this TemplateContexte instance.

        :param str text: The text to parse
        :return: The parsed text
        :rtype: str
        """

        start_marker = self.internals['StartMarker']
        end_marker = self.internals['EndMarker']

        def check_and_replace(match):
            varname = match.group(1)
            val = self.get_symbol_value(varname)

            # process filters (aka functions)
            if match.groups()[1] is not None:
                filters = match.group(2).split('!')

                if len(filters) == 0:
                    self.raise_exception('Invalid filter: %s' % varname)

                for filter in filters:
                    if filter == '':
                        continue

                    filter = filter.strip()
                    val = self.visit(AST.Function(filter, [AST.RAW(val)]))

            if not isinstance(val, str):
                val = str(val)

            return val

        # Match either start of string followed by StartMarker or anything but a backslash
        # Do not capture the first two group
        re_start_marker = re.escape(start_marker)
        p = re.compile(r'(?:(?:\A)|(?<=[^\\])){start_marker}\s*([\w\@]+)\s*(!.*)?\s*{end_marker}'.format(
            start_marker=re_start_marker,
            end_marker = end_marker
            ), re.MULTILINE)

        text = p.sub(check_and_replace, text)

        # Process remaining esacped characters
        text = text.replace('\\' + start_marker, start_marker)
        return text

    ############################################################
    # Extension handling
    ############################################################

    def add_function_lookup(self, lu):
        if isinstance(lu, list):
            self._function_lookup += lu
        else:
            self._function_lookup.append(lu)

    def add_builtin(self, symbol, val):
        self.builtins[symbol] = val


    ############################################################
    # Node visitors
    ############################################################

    def visit(self, node):
        method_name = 'visit_' + type(node).__name__.lower()
        visitor = getattr(self, method_name, self.fallback_visit)
        return visitor(node)

    def fallback_visit(self, node):
        self.raise_exception('No visitor found for node {0}'.format(node))

    def visit_raw(self, node: AST.RAW):
        # this node is used internally when a value does not need to be 
        # processed further

        return node.value

    def visit_function(self, node: AST.Function):
        funcname = node.name
        args = []

        for item in node.arglist:
            v = self.visit(item)
            
            args.append(v)

        call = None
        for f in self._function_lookup:
            if hasattr(f, '{0}'.format(funcname)):
                call = getattr(f, '{0}'.format(funcname))

        if call is not None:
            return call(args)
        else:
            self.raise_exception('Unknown function: {}'.format(funcname))

    def visit_sectionstart(self, node):

        if self.template_ctx is not None:
            # a template has already been processed - save it
            self.template_ctx.flush()
        
        self.template_ctx = TemplateContext()

    def visit_sectionend(self, node):
        pass

    def visit_null(self, node):
        pass

    def visit_internalassignment(self, node: AST.InternalAssignment):
        if not node.varname in self.allowed_internals:
            self.raise_exception('Unknown internal value {}'.format(node.varname))
        
        val = self.visit(node.value)

        if (not val in self.allowed_internals[node.varname]['allowed']) and \
            '*' not in self.allowed_internals[node.varname]['allowed']:
            self.raise_exception('Invalid value "{}" for internal setting {}'.format(val, node.varname))

        if node.varname == 'Output':
            self.template_ctx.output = val
        
        if node.varname == 'Filename':
            self.template_ctx.filename = val

    def visit_assignment(self, node: AST.Assignment):
        self.set_symbol_value(node.varname, self.visit(node.value))

    def visit_prompt(self, node: AST.Prompt):
        self.set_symbol_value(node.target_var, cli.user_input(node.text))

    def visit_collectionloop(self, node: AST.CollectionLoop):
        self.set_symbol_value(node.target_var, cli.collect(node.text))

    def visit_optionlist(self, node: AST.Optionlist):
        self.set_symbol_value(node.target_var, cli.choose(node.text, node.options))

    def visit_content(self, node: AST.Content):
        self.template_ctx.content.append(self.process_string(node.line))

    def visit_expression(self, node: AST.SimpleExpression):
        left = self.visit(node.left)
        right = self.visit(node.right)

        if node.operator == '==':
            return left == right
        elif node.operator == '!=':
            return left != right

    def visit_if(self, node: AST.If):
        e = self.visit_expression(node.condition)

        self.block_stack.push({
            'type': 'if',
            'condition': e,
            'block_resolved': e
        })

    def visit_value(self, node: AST.Value):
    
        if re.match(r'^\d+$', node.value):
            # integer
            return int(node.value)

        elif re.match(r'^\d+\.\d+$', node.value):
            # float
            return float(node.value)

        elif self.string_re.match(node.value):
            # string
            match = self.string_re.match(node.value)
            v = ''

            # depending on the delimiter, a different group will match
            if match.groups()[0] == None:
                v = match.groups()[1]
            else:
                v = match.groups()[0]

            # we automatically replace variables in string values
            v = self.process_string(v)
            return v
        
        else:
            # try builtin
            if node.value.lower() in self.builtins:
                return self.builtins[node.value.lower()]
            else:
                return self.get_symbol_value(node.value)
    
    def visit_else (self, node: AST.Else):

        try:
            elem = self.block_stack.get_first()

            if elem['type'] != 'if':
                self.raise_exception('Encountered ELSE without preceding IF')        
                
            if not elem['block_resolved']:
                elem['condition'] = not elem['condition']
                
            else:
                elem['condition'] = False

            self.block_stack.update_first(elem)

        except BlockStackEmptyException:
            self.raise_exception('Encountered ELSE without preceding IF (empty block stack)')
    
    def visit_elseif (self, node: AST.ElseIf):

        try:
            elem = self.block_stack.get_first()

            if elem['type'] != 'if':
                self.raise_exception('Encountered ELSE IF without preceding IF')

            e = False

            if not elem['block_resolved']:
                e = self.visit_expression(node.condition)
                elem['condition'] = e
                elem['block_resolved'] = e
            else:
                elem['condition'] = e
            
            self.block_stack.update_first(elem)

        except BlockStackEmptyException:
            self.raise_exception('Encountered ELSE IF without preceding IF (empty block stack)')

    def visit_endif (self, node: AST.Endif):

        try:
            elem = self.block_stack.get_first()

            if elem['type'] != 'if':
                self.raise_exception('Encountered ENDIF without preceding IF')        
                
            self.block_stack.pop()

        except BlockStackEmptyException:
            self.raise_exception('Encountered ENDIF without preceding IF (empty block stack)') 

    def visit_for(self, node: AST.For):
        listvar = self.visit(node.listvar)

        if not isinstance(listvar, list):
            self.raise_exception('Cannot iterate over variable "listvar" of type {}'.format(type(listvar)))

        if len(listvar) == 0:
            # list is empty. No need to create a loop.
            return

        self.set_symbol_value(node.itemvar, listvar[0])

        self.block_stack.push({
            'type': 'for',
            'listvar': listvar,
            'itemvar': node.itemvar,
            'pos': self.pos,
            'index': 0
        })

    def visit_endfor(self, node: AST.EndFor):

        try:
            elem = self.block_stack.get_first()

            if elem['type'] != 'for':
                self.raise_exception('Encountered ENDFOR without preceding FOR')        
                
            if elem['index'] == len(elem['listvar']) - 1:
                # end loop
                self.block_stack.pop()
            else:
                # next item
                elem['index'] += 1
                self.set_symbol_value(elem['itemvar'], elem['listvar'][elem['index']])
                self.block_stack.update_first(elem)

                # jump to next iteration
                self.pos = elem['pos']

        except BlockStackEmptyException:
            self.raise_exception('Encountered ENDFOR without preceding FOR (empty block stack)') 


    def visit_echo (self, node: AST.Echo):
        print(node.text)