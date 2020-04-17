#
# Contemply - A code generator that creates boilerplate files from templates
#
# Copyright (C) 2019-2020  Sean Mertiens
# For more information on licensing see LICENSE file
#

from contemply import cli
from contemply.parser import get_secure_path
from contemply.simple_interpreter import Interpreter
import contemply.simple_ast as AST
from colorama import Fore, Style
import re
import os
import logging

__all__ = ['SectionContext', 'Parser']

class SimpleExpression:

    def __init__(self, var, op, val):
        self.variable = var
        self.operator = op
        self.value = val

class LoopContext:

    def __init__(self, listvar, itemvar, target_line):
        self.listvar = listvar
        self.itemvar = itemvar
        self.target_line = target_line
        self.iteration = 0

class SectionContext:

    def __init__(self):

        self.data = {}
        self.settings = {
            'Output': None,
            'StartMarker': '§',
            'EndMarker': '§'
        }
        self.instructions_start = 0
        self.instructions_end = 0
        self.output = []

    def config_set(self, name, val):
        self.settings[name] = val

    def data_set(self, name, val):
        self.data[name] = val

    def add_output(self, line: str):
        self.output.append(line)

    def data_has(self, name):
        return name in self.data

    def data_get(self, name, default = None):
        try:
            return self.data[name]
        except KeyError:
            return default

    def data_remove(self, name):
        del self.data[name]

    def config_get(self, name, default = None):
        try:
            return self.settings[name]
        except KeyError:
            return default

    def write_output(self):
        
        filename = ''
        
        if self.config_get('Output') is None:
            
            while filename == '':
                filename = cli.user_input('Enter filename for saving [Press Ctrl + C to cancel]: ')

        elif self.config_get('Output') == '@null':
            return


        elif self.config_get('Output') == '@console':
            print('\n'.join(self.output))
            return

        else:
            filename = self.config_get('Output')

        path = get_secure_path(os.getcwd(), filename)
        disp_path = path.replace(os.getcwd(), '')

        overwrite = True
        if os.path.exists(path):
            overwrite = cli.prompt('A file with the name {0} already exists. Overwrite?'.format(disp_path))

        if overwrite:
            with open(path, 'w') as f:
                f.write('\n'.join(self.output))

        print(Fore.GREEN + '√' + Fore.RESET + ' File ' + Style.BRIGHT + '{0}'.format(disp_path) +
                Style.RESET_ALL + ' has been created')

class ParserException(Exception):
    pass


class Parser:

    SECTION_START = '--- Contemply'
    SECTION_END = '---'
    
    IF_START = '?'
    ELSE_IF_START = '??'

    SCOPE_SECTION_HEADER = 1
    SCOPE_CONTENT = 2

    def __init__(self):

        self.filename = ''
        self.lines = []
        self.current_line = 0

        self.scope = self.SCOPE_SECTION_HEADER

        self.block_stack = []

        # Regex for parsing section headers
        self.re_prompt = re.compile(r'^(\w+)(?:[ ]*)\:(?:[ ]*)(.*)$')
        self.re_assignment = re.compile(r'^(\w+)(?:[ ]*)=(?:[ ]*)(.*)$')
        self.re_option = re.compile(r'^(?:\t| +)\- (.*)$')
        self.re_repeat = re.compile(r'^(?:\t| +)\.\.\.$')

        re_internal = '|'.join(SectionContext().settings.keys())
        self.re_internal_assignment = re.compile(
            r'^(' + re_internal + ') is (.*)$')

        # Regex for processing lines - uncompiled in case start/end markers change
        if_base = r'\s*(\w+)\s*(\!\=|\=\=)?\s*(.+)?$'

        self.re_loop_start = r'^\s*{start}\s*(\w+)\s*\-\>\s*(\w+)\s*{end}$'
        self.re_if = re.compile(r'^\?' + if_base)
        self.re_else_if = re.compile(r'^\?\?' + if_base)
        self.re_block_end = r'^{start}\s*end\.\s*{end}'
        self.re_block_else = r'^{start}\s*else\?\s*{end}'

        # Base
        self.re_string = re.compile(r'^\"([^\"]+)\"$')

    def get_logger(self):
        """
        Returns the logger instance for the parser.
        This log level will also be used for the tokenizer and interpreter.

        :returns: Logger instance
        :rtype: logging.Logger
        """
        return logging.getLogger(self.__module__)

    def raise_exception(self, msg):
        raise ParserException('{} in {} on line {}'.format(msg, self.filename, self.current_line + 1))

    def advance_line(self):
        self.current_line += 1

    def parse_string(self, text: str):
        self.lines = text.splitlines()
        return self.parse()

    def parse_file(self, filename):
        """
        Parses the given filename

        :param str filename: The path to a file to parse
        :return: A list containing the lines of the parsed template
        :rtype: list
        """
        self.filename = filename

        with open(filename, 'r') as f:
            self.lines = f.read().splitlines()

        return self.parse()

    def check_scope_header(self):
        if self.scope != self.SCOPE_SECTION_HEADER:
            self.raise_exception('The expression may only be used inside a section header')

    def parse(self):
        # Validate first line
        # Must be: --- Contemply

        if (self.lines[0].rstrip() != self.SECTION_START):
            self.raise_exception('First line in template must start with ' + self.SECTION_START)
            return

        parse_tree = []

        while(self.current_line < len(self.lines)):
            line = self.lines[self.current_line]
            token = None

            # skip blank lines in header
            if (self.scope == self.SCOPE_SECTION_HEADER) and line.split() == '':
                self.advance_line()
                continue
            
            if line.rstrip() == self.SECTION_START:
                self.scope = self.SCOPE_SECTION_HEADER
                token = AST.SectionStart()

            elif line.rstrip() == self.SECTION_END:
                self.scope = self.SCOPE_CONTENT
                token = AST.SectionEnd()

            elif self.line_is_prompt():
                self.check_scope_header()

                if (self.line_is_option(1)):
                    token = self.process_optionlist()
                elif (self.line_is_loop(1)):
                    token = self.process_collection()
                else:
                    token = self.process_prompt()

            elif self.line_is_internal_assignment():
                self.check_scope_header()

                token = self.process_internal_assignment()

            elif self.line_is_assignment():
                self.check_scope_header()

                token = self.process_assignment()
            
            elif line.startswith(self.ELSE_IF_START):
                # try else
                if line.rstrip() == self.ELSE_IF_START:
                    token = AST.Else()

                # try else if
                else:
                    match = re.match(self.re_if_start, line)

                    if (match):
                        token = AST.ElseIf(match)
                    else:
                        self.raise_exception('Could not parse condition for else-if-clause')

            elif line.startswith(self.IF_START):
                # try endif
                if line.rstrip() == self.IF_START:
                    token = AST.Endif()
                else:
                    token = self.parse_if()

            else:
                if self.scope == self.SCOPE_CONTENT:
                    token = AST.Content(line)
                else:
                    token = self.process_echo()
            
            parse_tree.append(token)
            self.advance_line()
        
        intr = Interpreter()
        intr.run(parse_tree)
        return parse_tree
                
                

    def parse0(self):
        # Validate first line
        # Must be: --- Contemply

        if (self.lines[0].rstrip() != self.SECTION_START):
            self.raise_exception('First line in template must start with ' + self.SECTION_START)
            return

        self._ctx = SectionContext()
        self.flushed = True

        while(self.current_line < len(self.lines)):
            line = self.lines[self.current_line]

            if (len(self.block_stack) > 0) and (self.block_stack[0][0] == 'if') and not self.line_is_block_end():
                if not self.evaluate(self.block_stack[0][1]):
                    self.advance_line()
                    continue

            if line.rstrip() == self.SECTION_START:
                if not self.flushed:
                    self._ctx.write_output()
                    self.flushed = True
                
                self.advance_line()
                self.process_section_header()
                self.advance_line()

            if self.line_is_block_end():
                self.process_block_end()
                self.advance_line()

            elif self.line_is_loop_start():
                self.process_loop_start()
                
                # no advance line: after loop starts loop processing
                # will automatically set the current line to the first line
                # in the loop (that is: the next line)

            elif self.line_is_if_start():
                self.process_if_start()
                self.advance_line()

            else:
                self.process_line()

            if self.current_line >= (len(self.lines) - 1):
                self._ctx.write_output()

            self.advance_line()

    def line_is_block_end(self):
        rec = re.compile(self.re_block_end.format(
            start = re.escape(self._ctx.settings['StartMarker']),
            end = re.escape(self._ctx.settings['EndMarker'])
        ))

        return rec.match(self.lines[self.current_line])

    def line_is_loop_start(self):
        rec = re.compile(self.re_loop_start.format(
            start = re.escape(self._ctx.settings['StartMarker']),
            end = re.escape(self._ctx.settings['EndMarker'])
        ))

        return rec.match(self.lines[self.current_line])

    def line_is_if_start(self):
        rec = re.compile(self.re_if_start.format(
            start = re.escape(self._ctx.settings['StartMarker']),
            end = re.escape(self._ctx.settings['EndMarker'])
        ))

        return rec.match(self.lines[self.current_line])

    def process_loop_iteration(self, loop_ctx: LoopContext):
            listvar = self._ctx.data_get(loop_ctx.listvar)
            i = loop_ctx.iteration

            if listvar == None:
                self.raise_exception('Variable not found: ' + loop_ctx.listvar)
            
            if i >= len(listvar):
                # end loop
                self.block_stack.pop(0)

                # remove itemvar
                self._ctx.data_remove(loop_ctx.itemvar)
            else:
                self._ctx.data_set(loop_ctx.itemvar, listvar[i])
                loop_ctx.iteration += 1
                self.current_line = loop_ctx.target_line

    def check_if_left(self, val: str):
        val = val.strip()

        if not self._ctx.data_has(val):
            self.raise_exception('Variable not found: ' + val)
        else:
            return val

    def check_operator (self, op: str):
        op = op.strip()
        valid = ['!=', '==']

        if op not in valid:
            self.raise_exception('Invalid operator: ' + op)
        else:
            return op

    def check_if_right (self, val: str):
        val = val.strip()
        
        if self.re_string.match(val):
            match = self.re_string.match(val)
            return match.group(1)
        
        return val

    def parse_if(self):
        match = self.re_if.match(self.lines[self.current_line])

        if not match:
            self.raise_exception('Could not parse if-expression.')
        
        ex = None 

        # simple truth testing with only symbol
        if len(match.groups()) == 1:
            ex = AST.SimpleExpression(match.group(1), '==', AST.Value('True'))
        elif len(match.groups()) == 3:
            ex = AST.SimpleExpression(match.group(1), match.group(2), match.group(3))
        else:
            self.raise_exception('Could not parse if-expression. Unexpected number of groups.')

        return AST.If(ex)

    def process_loop_start(self):
        rec = re.compile(self.re_loop_start.format(
            start = re.escape(self._ctx.settings['StartMarker']),
            end = re.escape(self._ctx.settings['EndMarker'])
        ))

        match = rec.match(self.lines[self.current_line])
        listvar = match.group(1)
        itemvar = match.group(2)

        ctx = LoopContext(listvar, itemvar, self.current_line)
        self.block_stack.insert(0, ['loop', ctx])
        self.process_loop_iteration(ctx)

    def evaluate(self, exp: SimpleExpression) -> bool:
        left = self._ctx.data_get(exp.variable)

        if (exp.operator == '=='):
            return left == exp.value
        elif  (exp.operator == '!='):
            return left != exp.value
        else:
            self.throw_exception('Error processing expression.')

    def process_block_end(self):
        if (len(self.block_stack) == 0):
            self.raise_exception('Unexpected end of block.')

        current_block = self.block_stack[0]

        if current_block[0] == 'loop':
            self.process_loop_iteration(current_block[1])
        elif current_block[0] == 'if':
            self.block_stack.pop(0)

    def process_line(self):

        def replace(match):
            varname = match.group(1).strip()

            val = self._ctx.data_get(varname)

            if val == None:
                self.raise_exception('Variable not found: ' + varname)

            return val

        line = self.lines[self.current_line]

        elem_re = re.compile(r'{start}([^{start}{end}]*){end}'.format(
            start = re.escape(self._ctx.settings['StartMarker']),
            end = re.escape(self._ctx.settings['EndMarker'])
        ))

        self.flushed = False
        matches = elem_re.sub(replace, line)
        self._ctx.add_output(matches)


    def line_is_loop(self, lookahead=0):
        if (self.current_line + lookahead) >= len(self.lines):
            return False

        return self.re_repeat.match(self.lines[self.current_line + lookahead])

    def line_is_internal_assignment(self, lookahead=0):
        if (self.current_line + lookahead) >= len(self.lines):
            return False

        return self.re_internal_assignment.match(self.lines[self.current_line + lookahead])

    def line_is_assignment(self, lookahead=0):
        if (self.current_line + lookahead) >= len(self.lines):
            return False

        return self.re_assignment.match(self.lines[self.current_line + lookahead])

    def line_is_prompt(self, lookahead=0):
        if (self.current_line + lookahead) >= len(self.lines):
            return False

        return self.re_prompt.match(self.lines[self.current_line + lookahead])

    def line_is_option(self, lookahead=0):
        if (self.current_line + lookahead) >= len(self.lines):
            return False

        return self.re_option.match(self.lines[self.current_line + lookahead])

    def process_section_header(self):

        nodes = []
        
        while(self.lines[self.current_line].rstrip() != self.SECTION_END):
            node = None
        
            if self.line_is_prompt():
                if (self.line_is_option(1)):
                    node = self.process_optionlist()
                elif (self.line_is_loop(1)):
                    node = self.process_collection()
                else:
                    node = self.process_prompt()

            elif self.line_is_internal_assignment():
                node = self.process_internal_assignment()

            elif self.line_is_assignment():
                node = self.process_assignment()

            else:
                node = self.process_echo()

            if self.current_line == (len(self.lines) - 1):
                self.raise_exception('Missing section end marker') 

            self.advance_line()

            if node is None:
                self.raise_exception('Unexpected input')
            else:
                if not isinstance(node, AST.Null):
                    nodes.append(node)

        return AST.SectionHeader(nodes)
        
    def process_prompt(self):
        match = self.re_prompt.match(self.lines[self.current_line])
        return AST.Prompt(match.group(1), match.group(2))

    def process_collection(self):
        match = self.re_prompt.match(self.lines[self.current_line])
        self.advance_line()
        return AST.CollectionLoop(match.group(2), match.group(1))

    def process_internal_assignment(self):
        match = self.re_internal_assignment.match(self.lines[self.current_line])
        return AST.InternalAssignment(match.group(1), match.group(2))
 
    def process_assignment(self):
        match = self.re_assignment.match(self.lines[self.current_line])
        return AST.Assignment(match.group(1), match.group(2))

    def process_optionlist(self):
        prompt = self.re_prompt.match(self.lines[self.current_line])
        self.advance_line()

        options = []

        while (True):
            if self.line_is_option():
                options.append(self.re_option.match(
                    self.lines[self.current_line]).group(1))

                if (self.line_is_option(1)):
                    self.advance_line()
                else:
                    break
            else:
                break
        
        return AST.Optionlist(prompt.group(2), options, prompt.group(1))

    def process_echo(self):
        if self.lines[self.current_line].strip() != '':
            return AST.Echo(self.lines[self.current_line])
        else:
            return AST.Null()



if __name__ == "__main__":
    p = Parser()
    f = '/Users/mephisto/python_projects/contemply/src/contemply/samples/class.pytpl'

    p.parse_file(f)