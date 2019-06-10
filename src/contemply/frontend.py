#
# Contemply - A code generator that creates boilerplate files from templates
#
# Copyright (C) 2019  Sean Mertiens
# For more information on licensing see LICENSE file
#
import os, logging
import contemply.cli as cli
from colorama import Fore, Style
from contemply.storage import get_secure_path
from contemply.interpreter import Interpreter
from contemply.parser import TemplateContext, Parser
from contemply.tokenizer import Tokenizer

class TemplateParser:
    """
    This is the frontend class used for TemplateParsing.
    It will set up a TemplateContext and split the input text up in
    separate lines before handing it to the _parse function.
    """

    OUTPUTMODE_CONSOLE, OUTPUTMODE_FILE = 0, 1

    def __init__(self):
        self._ctx = TemplateContext()
        self._output_mode = self.OUTPUTMODE_FILE
        self._lookup_modules = []
        self._additional_builtins = {}

    def get_logger(self):
        """
        Returns the logger instance for the parser.
        This log level will also be used for the tokenizer and interpreter.

        :returns: Logger instance
        :rtype: logging.Logger
        """
        return logging.getLogger(self.__module__)

    def get_template_context(self):
        """
        Returns the current template context instance

        :return: The current template context
        :rtype: TemplateContext
        """
        return self._ctx

    def set_output_mode(self, mode):
        """
        Sets the parsers output mode. If set to "console", the parsed template is output to the
        console. Defaults to OUTPUTMODE_FILE.

        :param mode: TemplateParser.OUTPUTMODE_CONSOLE | TemplateParser.OUTPUTMODE_FILE
        """
        self._output_mode = mode

    def register_lookup_module(self, mod):
        if hasattr(mod, 'builtins'):
            for symbol, val in mod.builtins.items():
                self._additional_builtins[symbol] = val

        self._lookup_modules.append(mod)

    def parse_file(self, filename):
        """
        Parses the given filename

        :param str filename: The path to a file to parse
        :return: A list containing the lines of the parsed template
        :rtype: list
        """
        self._ctx.set_filename(os.path.basename(filename))

        with open(filename, 'r') as f:
            lines = f.read()

        self._ctx.set_text(lines)

        return self.parse()

    def parse(self, text=None):
        """
        Parses the given text. If no text is set, the parser will parse the content of the current
        TemplateContext.

        :param str text: A text to parse
        :return: A list containing the lines of the parsed template
        :rtype: list
        """
        if text is not None:
            self._ctx.set_text(text)
            self._ctx.set_filename('')

        # Create the Tokenizer, Parser and Interpreter instances
        tokenizer = Tokenizer(self._ctx)
        tokenizer.get_logger().setLevel(self.get_logger().level)
        parser = Parser(tokenizer, self._ctx)
        interpreter = Interpreter(self._ctx)
        interpreter.get_logger().setLevel(self.get_logger().level)

        # register modules
        interpreter.add_function_lookup(self._lookup_modules)

        for symbol, val in self._additional_builtins.items():
            interpreter.add_builtin(symbol, val)

        # parse the input and create a AST
        tree = parser.parse()
        # interpret the AST and execute all statements contained within
        interpreter.interpret(tree)

        # result will hold the contents of the parsed template
        result = interpreter.get_parsed_template()

        if self._output_mode == TemplateParser.OUTPUTMODE_FILE:
            for target_file, content in result.items():
                if target_file == Interpreter.DEFAULT_TARGET:
                    # The default target will only be created if the content is not empty.
                    if len(content) == 0:
                        continue

                    # In case setOutput is used - will be deprecated in some future release
                    if self._ctx.outputfile() != '':
                        target_file = self._ctx.outputfile()
                    else:
                        # Prompt for outputfile
                        target_file = cli.user_input('Please enter the filename of the new file: ')

                target_file = self._ctx.process_variables(target_file)
                path = get_secure_path(os.getcwd(), target_file)
                disp_path = target_file.replace(os.getcwd(), '')

                overwrite = True
                if os.path.exists(path):
                    overwrite = cli.prompt('A file with the name {0} already exists. Overwrite?'.format(disp_path))

                if overwrite:
                    with open(path, 'w') as f:
                        f.write('\n'.join(content))

                print(Fore.GREEN + '√' + Fore.RESET + ' File ' + Style.BRIGHT + '{0}'.format(disp_path) +
                      Style.RESET_ALL + ' has been created')

        elif self._output_mode == self.OUTPUTMODE_CONSOLE:
            for target_file, content in result.items():
                if target_file == Interpreter.DEFAULT_TARGET:
                    target_file = self._ctx.outputfile() if self._ctx.outputfile() != '' else '(No filename specified)'
                else:
                    target_file = target_file.replace(os.getcwd(), '')

                print(Fore.CYAN + target_file + ': ' + Fore.RESET)

                for line in content:
                    print('\t' + line)

        return result
