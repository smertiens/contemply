#
# Contemply - A code generator that creates boilerplate files from templates
#
# Copyright (C) 2019  Sean Mertiens
# For more information on licensing see LICENSE file
#

from contemply.parser import *


def test_parser_simple():
    text = '#: var1 = "Hello"\n#: var2 = "World"\n$var1 $var2'
    parser = TemplateParser()
    parser.set_output_mode(TemplateParser.OUTPUTMODE_CONSOLE)
    result = parser.parse(text)

    assert result == ['Hello World']
    assert parser.get_template_context().get('var1') == 'Hello'
    assert parser.get_template_context().get('var2') == 'World'


def test_parser_if():
    text = [
        '#: var1 = "Hello"',
        '#: var2 = "Hello"',
        '#: if var1 == var2',
        'Lorem ipsum',
        'or something',
        '#: endif'
    ]

    parser = TemplateParser()
    parser.set_output_mode(TemplateParser.OUTPUTMODE_CONSOLE)
    result = parser.parse('\n'.join(text))
    assert result == ['Lorem ipsum', 'or something']

    text[0] = '#: var1 = "Not Hello"'

    result = parser.parse('\n'.join(text))
    assert result == []


def test_parser_if_else():
    text = [
        '#: var1 = "Hello"',
        '#: var2 = "Not Hello"',
        '#: if var1 == var2',
        'Lorem ipsum',
        '#: else',
        'or something',
        '#: endif'
    ]

    parser = TemplateParser()
    parser.set_output_mode(TemplateParser.OUTPUTMODE_CONSOLE)
    result = parser.parse('\n'.join(text))
    assert result == ['or something']

    text[0] = '#: var1 = "Not Hello"'
    result = parser.parse('\n'.join(text))
    assert result == ['Lorem ipsum']

def test_parser_skip_comments():
    text = [
        '#% var1 = "Hello"',
        'Lorem ipsum',
        '# Comment'
    ]

    parser = TemplateParser()
    parser.set_output_mode(TemplateParser.OUTPUTMODE_CONSOLE)
    result = parser.parse('\n'.join(text))
    assert result == ['Lorem ipsum', '# Comment']
    assert not parser.get_template_context().has('var1')

