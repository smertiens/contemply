#
# Contemply - A code generator that creates boilerplate files from templates
#
# Copyright (C) 2019  Sean Mertiens
# For more information on licensing see LICENSE file
#

def islistempty(listvar):
    """
    Checks wether a list has only empty values.
    Empty values are empty strings ("") or None.

    :param list listvar:
    :return: True if empty, False otherwise
    :rtype: bool
    """

    has_empty = True
    empty = ("", None)
    for item in listvar:
        if item not in empty:
            has_empty = False

    return has_empty

def _get_native_type(def_type):
    type_map = {
        'str': str,
        'list': list,
        'int': int,
        'float': float,
        'bool': bool
    }

    if not def_type in type_map:
        raise Exception('Could not map type definition "{}"'.format(def_type))

    return type_map[def_type]


def check_function_args(definition, args):
    """
    Compares a list of arguments to a list of expected arguments.
    Raises an exception if the definitions don't match.

    Format:

        [Functionname, type, *type, ... ]

    * means this argument is optional

    :param list definition:
    :param list args:
    :raises: Exception
    """

    func_name = definition[0] + '()'
    definition = definition[1:]
    min_args_needed = 0
    optional_arg_encountered = False

    for arg in definition:
        if arg.startswith('*'):
            optional_arg_encountered = True
        else:
            if optional_arg_encountered:
                raise Exception('After an optional argument only further optional arguments are allowed.')

            min_args_needed += 1

    if len(args) < min_args_needed:
        raise Exception('{} expects at least {} arguments.'.format(func_name, min_args_needed))

    if len(args) > len(definition):
        raise Exception('{} accepts a maximum of {} arguments'.format(func_name, len(definition)))

    for n, def_type in enumerate(definition):
        optional = def_type.startswith('*')
        if optional:
            def_type = def_type[1:]

            if n > len(args) - 1:
                # optional argument not found in argument list
                continue

        def_type_list = [_get_native_type(item) for item in def_type.replace(' ', '').split(',')]

        if type(args[n]) not in def_type_list:
            raise Exception('{} expected {} as argument number {}'.format(func_name, def_type, n))
