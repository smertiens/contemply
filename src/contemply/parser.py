#
# Contemply - A code generator that creates boilerplate files from templates
#
# Copyright (C) 2019-2020  Sean Mertiens
# For more information on licensing see LICENSE file
#

import logging
import os
import re

from colorama import Fore, Style

import contemply.ast as AST
from contemply import cli
from contemply.storage import get_secure_path
from contemply.interpreter import Interpreter


class ParserException(Exception):
    pass

class Parser:

    SECTION_START = '--- Contemply'
    SECTION_END = '---'
    
    IF_START = '?'
    ELSE_IF_START = '??'
    LOOP_START = '...'
    FUNCTION_START = '!'

    SCOPE_SECTION_HEADER = 1
    SCOPE_CONTENT = 2

    def __init__(self):

        self.interpreter = Interpreter()
        self.filename = ''
        self.lines = []
        self.current_line = 0
        self.parse_tree = []

        self.scope = self.SCOPE_SECTION_HEADER

        self.block_stack = []

        # Regex for parsing section headers
        self.re_prompt = re.compile(r'^(\w+)\s*\:\s*(?:(?:\"([^\"]*)\")|(?:\'([^\']*)\'))$')
        self.re_assignment = re.compile(r'^(\w+)(?:[ ]*)=(?:[ ]*)(.*)$')
        self.re_option = re.compile(r'^(?:\t| +)\- (.*)$')
        self.re_repeat = re.compile(r'^(?:\t| +)\.\.\.$')

        re_internal = '|'.join(Interpreter().allowed_internals.keys())
        self.re_internal_assignment = re.compile(
            r'^(' + re_internal + ') is (.*)$')

        # Regex for processing lines - uncompiled in case start/end markers change
        if_base = r'\s*(\w+)\s*(\!\=|\=\=)?\s*(.+)?$'

        self.re_for_loop = re.compile(r'^\.\.\.\s*(\w+)\s*\-\>\s*(\w+)$')
        self.re_if = re.compile(r'^\?' + if_base)
        self.re_else_if = re.compile(r'^\?\?' + if_base)
        self.re_function = re.compile(r'^\!\s*(\w+)\s*\((.*)\)$')
        self.re_function_args = re.compile(r'([\d\.]+)|\w+|(\"[^\"]+\")|(\'[^\']+\')(?:,?)')

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

        self.parse_tree = []

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
                    token = self.parse_optionlist()
                elif (self.line_is_loop(1)):
                    token = self.parse_collection()
                else:
                    token = self.parse_prompt()

            elif self.line_is_internal_assignment():
                self.check_scope_header()

                token = self.parse_internal_assignment()

            elif self.line_is_assignment():
                self.check_scope_header()

                token = self.parse_assignment()
            
            elif line.startswith(self.ELSE_IF_START):
                # try else
                if line.rstrip() == self.ELSE_IF_START:
                    token = AST.Else()

                # try else if
                else:
                    token = self.parse_else_if()

            elif line.startswith(self.IF_START):
                # try endif
                if line.rstrip() == self.IF_START:
                    token = AST.Endif()
                else:
                    token = self.parse_if()

            elif line.startswith(self.LOOP_START):
                # try endloop
                if line.rstrip() == self.LOOP_START:
                    token = AST.EndFor()
                else:
                    token = self.parse_for()

            elif line.startswith(self.FUNCTION_START):
                token = self.parse_function()

            else:
                if self.scope == self.SCOPE_CONTENT:
                    token = AST.Content(line)
                else:
                    token = self.parse_echo()
            
            self.parse_tree.append(token)
            self.advance_line()
        
        return self.parse_tree

    def parse_function(self):
        match = self.re_function.match(self.lines[self.current_line])

        if not match:
            self.raise_exception('Could not parse function-expression.')

        funcname = match.group(1)
        args = match.group(2)
        arglist = []

        if args != '':
            arg_matches = self.re_function_args.finditer(args)

            for m in arg_matches:
                val = None

                for n in m.groups():
                    if n is not None:
                        val = AST.Value(n)

                if val is None:
                    self.raise_exception('Could not parse function argument list: %s' % args)

                arglist.append(val)

        return AST.Function(funcname, arglist)

    def parse_if(self):
        match = self.re_if.match(self.lines[self.current_line])

        if not match:
            self.raise_exception('Could not parse if-expression.')
        
        ex = None 

        # simple truth testing with only symbol
        if len(match.groups()) == 1:
            ex = AST.SimpleExpression(AST.Value(match.group(1)), '==', AST.Value('True'))
        elif len(match.groups()) == 3:
            ex = AST.SimpleExpression(AST.Value(match.group(1)), match.group(2), AST.Value(match.group(3)))
        else:
            self.raise_exception('Could not parse if-expression. Unexpected number of groups.')

        return AST.If(ex)


    def parse_else_if(self):
        match = self.re_else_if.match(self.lines[self.current_line])

        if not match:
            self.raise_exception('Could not parse else if-expression.')
        
        ex = None 

        # simple truth testing with only symbol
        if len(match.groups()) == 1:
            ex = AST.SimpleExpression(AST.Value(match.group(1)), '==', AST.Value('True'))
        elif len(match.groups()) == 3:
            ex = AST.SimpleExpression(AST.Value(match.group(1)), match.group(2), AST.Value(match.group(3)))
        else:
            self.raise_exception('Could not parse if-expression. Unexpected number of groups.')

        return AST.ElseIf(ex)


    def parse_for(self):
        match = self.re_for_loop.match(self.lines[self.current_line])
        return AST.For(AST.Value(match.group(1)), match.group(2))

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
        
    def parse_prompt(self):
        match = self.re_prompt.match(self.lines[self.current_line])

        prompt = match.group(1)
        text = ''

        if match.groups()[1] is not None:
            text = match.group(2)
        else:
            text = match.group(3)

        # add " to the text, so the value visitor will recognize it as string
        # and preform variale replacement
        return AST.Prompt(AST.Value('"' + text + '"'), prompt)

    def parse_collection(self):
        match = self.re_prompt.match(self.lines[self.current_line])

        prompt = match.group(1)
        text = ''

        if match.groups()[1] is not None:
            text = match.group(2)
        else:
            text = match.group(3)

        self.advance_line()
        return AST.CollectionLoop(AST.Value('"' + text + '"'), prompt)

    def parse_internal_assignment(self):
        match = self.re_internal_assignment.match(self.lines[self.current_line])
        return AST.InternalAssignment(match.group(1), AST.Value(match.group(2)))
 
    def parse_assignment(self):
        match = self.re_assignment.match(self.lines[self.current_line])
        return AST.Assignment(match.group(1), AST.Value(match.group(2)))

    def parse_optionlist(self):
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

    def parse_echo(self):
        if self.lines[self.current_line].strip() != '':
            return AST.Echo(self.lines[self.current_line])
        else:
            return AST.Null()

    def run(self):
        
        self.interpreter.run(self.parse_tree)

if __name__ == "__main__":
    p = Parser()
    intr = Interpreter()

    f = '/Users/mephisto/python_projects/contemply/src/contemply/samples/class.pytpl'
    parse_tree = p.parse_file(f)
    p.run()