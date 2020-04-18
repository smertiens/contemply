#
# Contemply - A code generator that creates boilerplate files from templates
#
# Copyright (C) 2019  Sean Mertiens
# For more information on licensing see LICENSE file
#

from contemply.frontend import TemplateParser
from contemply.interpreter import Interpreter

def test_subtraction():
    parser = TemplateParser()
    parser.set_output_mode(TemplateParser.OUTPUTMODE_CONSOLE)
    result = parser.parse('#: result = 1283 - 87\n$result')[Interpreter.DEFAULT_TARGET]
    assert result == ['1196']


def test_addition():
    parser = TemplateParser()
    parser.set_output_mode(TemplateParser.OUTPUTMODE_CONSOLE)
    result = parser.parse('#: result = 274 + 863\n$result')[Interpreter.DEFAULT_TARGET]
    assert result == ['1137']


def test_division():
    parser = TemplateParser()
    parser.set_output_mode(TemplateParser.OUTPUTMODE_CONSOLE)
    result = parser.parse('#: result =  285/5\n$result')[Interpreter.DEFAULT_TARGET]
    #TODO: There are only int numbers in contemply... so that should not be the correct result
    assert result == ['57.0']


def test_multiplication():
    parser = TemplateParser()
    parser.set_output_mode(TemplateParser.OUTPUTMODE_CONSOLE)
    result = parser.parse('#: result =  1839 * 123\n$result')[Interpreter.DEFAULT_TARGET]
    assert result == ['226197']
