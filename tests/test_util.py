#
# Contemply - A code generator that creates boilerplate files from templates
#
# Copyright (C) 2019  Sean Mertiens
# For more information on licensing see LICENSE file
#

import pytest
from contemply import util

def test_check_function_len_okay():
    util.check_function_args(['myfunc', 'str', 'str'], ['hello', 'world'])
    util.check_function_args(['myfunc', 'str', '*str'], ['hello', 'world'])
    util.check_function_args(['myfunc', 'str', '*str', '*str, list'], ['hello', 'world'])

def test_check_function_len_too_much():
    with pytest.raises(Exception):
        util.check_function_args(['myfunc', 'str', 'str'], ['hello', 'world', 'demo'])

    with pytest.raises(Exception):
        util.check_function_args(['myfunc', 'str', 'str', '*str'], ['hello', 'world', 'demo', 'test'])

def test_check_function_len_too_less():
    with pytest.raises(Exception):
        util.check_function_args(['myfunc', 'str', 'str'], ['hello'])

    with pytest.raises(Exception):
        util.check_function_args(['myfunc', 'str', 'str', '*str'], ['hello'])

def test_check_function_types():
    util.check_function_args(['myfunc', 'str', 'str'], ['hello', 'world'])
    util.check_function_args(['myfunc', 'int', 'str'], [1233, 'world'])
    util.check_function_args(['myfunc', 'int', 'str', '*float'], [1233, 'world', 0.22323])
    util.check_function_args(['myfunc', 'int', 'list', '*float'], [1233, ['world']])
    util.check_function_args(['myfunc', 'int, bool', 'list', '*float, bool'], [1233, ['world'], True])

    with pytest.raises(Exception):
        util.check_function_args(['myfunc', 'int, bool'], [['world']])

    with pytest.raises(Exception):
        util.check_function_args(['myfunc', 'int'], [23.309])

    with pytest.raises(Exception):
        util.check_function_args(['myfunc', 'int', '*bool'], [23, 'True'])
