#
# Contemply - A code generator that creates boilerplate files from templates
#
# Copyright (C) 2019-2020  Sean Mertiens
# For more information on licensing see LICENSE file
#

import importlib
from contemply.exceptions import BundleException

class ParserEnvironment:

    def __init__(self):
        self.function_lookups = []
        self.builtins = {}

    def load_extension(self, modname):
        """
        To load an extension, provide the name of a python module.
        The module has to contain a "cpy_extension.py" that holds
        all the available functions and builtins for this extension.

        :param modname: The python module to load as an extension
        """

        try:
            mod = importlib.import_module(modname + '.cpy_extension')

            if hasattr(mod, 'builtins'):
                for symbol, val in mod.builtins.items():
                    self.builtins[symbol] = val
            
            self.function_lookups.append(mod)

        except ImportError:
            raise BundleException("The module '%s' is not a valid contemply bundle." % modname)

    def get_registered_functions(self):
        return self.function_lookups

    def get_registered_builtins(self):
        return self.builtins