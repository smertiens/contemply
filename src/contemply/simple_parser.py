from contemply import cli
from contemply.parser import get_secure_path
from colorama import Fore, Style
import re
import os
import logging

__all__ = ['SectionContext', 'Parser']

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

    def __init__(self):

        self.filename = ''
        self.lines = []
        self.current_line = 0

        # Regex for parsing section headers
        self.re_prompt = re.compile(r'^(\w+)(?:[ ]*)\:(?:[ ]*)(.*)$')
        self.re_assignment = re.compile(r'^(\w+)(?:[ ]*)=(?:[ ]*)(.*)$')
        self.re_option = re.compile(r'^(?:\t| +)\- (.*)$')
        self.re_repeat = re.compile(r'^(?:\t| +)\.\.\.$')

        re_internal = '|'.join(SectionContext().settings.keys())
        self.re_internal_assignment = re.compile(
            r'^(' + re_internal + ') is (.*)$')

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

    def parse(self):
        # Validate first line
        # Must be: --- Contemply

        if (self.lines[0].rstrip() != self.SECTION_START):
            self.raise_exception('First line in template must start with ' + self.SECTION_START)
            return

        self._ctx = SectionContext()
        self.flushed = True

        while(self.current_line < len(self.lines)):
            line = self.lines[self.current_line]

            if line.rstrip() == self.SECTION_START:
                if not self.flushed:
                    self._ctx.write_output()
                    self.flushed = True
                
                self.advance_line()
                self.process_section_header()
            else:
                self.process_line()

            if self.current_line == (len(self.lines) - 1):
                self._ctx.write_output()

            self.advance_line()

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

    def process_section_header(self):

        while(self.lines[self.current_line].rstrip() != self.SECTION_END):

            if self.line_is_prompt():
                if (self.line_is_option(1)):
                    self.process_optionlist()
                elif (self.line_is_repetition(1)):
                    self.process_collection()
                else:
                    self.process_prompt()

            elif self.line_is_internal_assignment():
                self.process_internal_assignment()

            elif self.line_is_assignment():
                self.process_assignment()

            else:
                self.line_echo()

            if self.current_line == (len(self.lines) - 1):
                self.raise_exception('Missing section end marker') 

            self.advance_line()

    def process_collection(self):
        match = self.re_prompt.match(self.lines[self.current_line])
        self.advance_line()

        self._ctx.data_set(match.group(1), cli.collect(match.group(2)))

    def line_is_repetition(self, lookahead=0):
        if (self.current_line + lookahead) >= len(self.lines):
            return False

        return self.re_repeat.match(self.lines[self.current_line + lookahead])

    def line_is_internal_assignment(self, lookahead=0):
        if (self.current_line + lookahead) >= len(self.lines):
            return False

        return self.re_internal_assignment.match(self.lines[self.current_line + lookahead])

    def process_internal_assignment(self):
        match = self.re_internal_assignment.match(self.lines[self.current_line])

        self._ctx.config_set(match.group(1), match.group(2))

    def line_is_assignment(self, lookahead=0):
        if (self.current_line + lookahead) >= len(self.lines):
            return False

        return self.re_assignment.match(self.lines[self.current_line + lookahead])

    def process_assignment(self):
        match = self.re_assignment.match(self.lines[self.current_line])
        self._ctx.data_set(match.group(1), match.group(2))

    def process_optionlist(self):
        prompt = self.re_prompt.match(self.lines[self.current_line])
        self.advance_line()

        options = []

        while (True):
            if (self.line_is_option()):
                options.append(self.re_option.match(
                    self.lines[self.current_line]).group(1))

                if (self.line_is_option(1)):
                    self.advance_line()
                else:
                    break
            else:
                break

        self._ctx.data_set(prompt.group(1), cli.choose(prompt.group(2), options))

    def line_echo(self):
        if self.lines[self.current_line].strip != '':
            print(self.lines[self.current_line])

    def line_is_prompt(self, lookahead=0):
        if (self.current_line + lookahead) >= len(self.lines):
            return False

        return self.re_prompt.match(self.lines[self.current_line + lookahead])

    def line_is_option(self, lookahead=0):
        if (self.current_line + lookahead) >= len(self.lines):
            return False

        return self.re_option.match(self.lines[self.current_line + lookahead])

    def process_prompt(self):
        match = self.re_prompt.match(self.lines[self.current_line])
        answer = cli.user_input(match.group(2) + ' ')

        self._ctx.data_set(match.group(1), answer)

if __name__ == "__main__":
    p = Parser()
    f = '/Users/mephisto/python_projects/contemply/src/contemply/samples/simple_sample.txt'

    p.parse_file(f)