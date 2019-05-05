#
# Contemply - A code generator that creates boilerplate files from templates
#
# Copyright (C) 2019  Sean Mertiens
# For more information on licensing see LICENSE file
#

from contemply.parser import *
import pytest


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


def test_while_loop():
    text = [
        '#: num = 0',
        '#: while num <= 5',
        'This run no. $num',
        '#: num = num + 1',
        '#: endwhile'
    ]

    expected = [
        'This run no. 0',
        'This run no. 1',
        'This run no. 2',
        'This run no. 3',
        'This run no. 4',
        'This run no. 5'
    ]

    parser = TemplateParser()
    parser.set_output_mode(TemplateParser.OUTPUTMODE_CONSOLE)
    result = parser.parse('\n'.join(text))
    assert result == expected


def test_while_loop_max_runs():
    text = [
        '#: while True',
        '#: endwhile'
    ]

    parser = TemplateParser()
    parser.set_output_mode(TemplateParser.OUTPUTMODE_CONSOLE)

    with pytest.raises(ParserError):
        parser.parse('\n'.join(text))


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


def test_subtraction():
    parser = TemplateParser()
    parser.set_output_mode(TemplateParser.OUTPUTMODE_CONSOLE)
    result = parser.parse('#: result = 1283 - 87\n$result')
    assert result == ['1196']


def test_addition():
    parser = TemplateParser()
    parser.set_output_mode(TemplateParser.OUTPUTMODE_CONSOLE)
    result = parser.parse('#: result = 274 + 863\n$result')
    assert result == ['1137']


def test_division():
    parser = TemplateParser()
    parser.set_output_mode(TemplateParser.OUTPUTMODE_CONSOLE)
    result = parser.parse('#: result =  285/5\n$result')
    assert result == ['57.0']


def test_multiplication():
    parser = TemplateParser()
    parser.set_output_mode(TemplateParser.OUTPUTMODE_CONSOLE)
    result = parser.parse('#: result =  1839 * 123\n$result')
    assert result == ['226197']
