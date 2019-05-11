#
# Contemply - A code generator that creates boilerplate files from templates
#
# Copyright (C) 2019  Sean Mertiens
# For more information on licensing see LICENSE file
#
from contemply.parser import *
import pytest

def test_list_index():
    parser = TemplateParser()
    parser.set_output_mode(TemplateParser.OUTPUTMODE_CONSOLE)
    result = parser.parse("#: list = ['item 1']\n#: echo(list[0])")


def test_list_add():
    parser = TemplateParser()
    parser.set_output_mode(TemplateParser.OUTPUTMODE_CONSOLE)
    result = parser.parse("#: list = ['item 1']\n#: list += 'item 2'")

    assert parser.get_template_context().get('list') == ['item 1', 'item 2']


def test_string():
    parser = TemplateParser()
    parser.set_output_mode(TemplateParser.OUTPUTMODE_CONSOLE)
    result = parser.parse("#: my_str = 'Hello World'")
    assert parser.get_template_context().get('my_str') == 'Hello World'

    result = parser.parse('#: my_str = "Hello World"')
    assert parser.get_template_context().get('my_str') == 'Hello World'

    result = parser.parse("#: my_str = 'Hello \"World\"'")
    assert parser.get_template_context().get('my_str') == 'Hello "World"'

    result = parser.parse('#: my_str = "Hello \'World\'"')
    assert parser.get_template_context().get('my_str') == "Hello 'World'"

    result = parser.parse('#: my_str = "Hello \'World\'"')
    assert parser.get_template_context().get('my_str') == "Hello 'World'"


def test_string_fail_if_not_terminated():
    parser = TemplateParser()
    parser.set_output_mode(TemplateParser.OUTPUTMODE_CONSOLE)

    with pytest.raises(SyntaxError):
        result = parser.parse("#: my_str = 'Hello World")


