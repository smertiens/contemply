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


def test_simple_expressions():
    text = [
        '#: test1 = 10',
        '#: test2 = 8',
        '#: test3 = 18',
        '#: result = 10 + 8',
        '#: if test3 == result',
        'Hello',
        '#: endif'
    ]

    parser = TemplateParser()
    parser.set_output_mode(TemplateParser.OUTPUTMODE_CONSOLE)
    result = parser.parse('\n'.join(text))
    assert result == ['Hello']

    text[2] = '#: test3 = 5'

    parser = TemplateParser()
    parser.set_output_mode(TemplateParser.OUTPUTMODE_CONSOLE)
    result = parser.parse('\n'.join(text))
    assert result == []


