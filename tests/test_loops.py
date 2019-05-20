#
# Contemply - A code generator that creates boilerplate files from templates
#
# Copyright (C) 2019  Sean Mertiens
# For more information on licensing see LICENSE file
#

import pytest
from contemply.parser import *


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


def test_nested_while_loop():
    text = [
        '#: outer = 0',
        '#: inner = 0',
        '#: while outer <= 3',
        'outer: $outer',
        '#: while inner <= 2',
        'inner: $inner',
        '#: inner = inner + 1',
        '#: endwhile',
        '#: inner = 0',
        '#: outer = outer + 1',
        '#: endwhile'
    ]

    parser = TemplateParser()
    parser.set_output_mode(TemplateParser.OUTPUTMODE_CONSOLE)
    result = parser.parse('\n'.join(text))
    assert ['outer: 0', 'inner: 0', 'inner: 1', 'inner: 2', 'outer: 1', 'inner: 0', 'inner: 1',
            'inner: 2', 'outer: 2', 'inner: 0', 'inner: 1', 'inner: 2', 'outer: 3',
            'inner: 0', 'inner: 1', 'inner: 2'] == result


def test_while_loop_max_runs():
    text = [
        '#: while True',
        '#: endwhile'
    ]

    parser = TemplateParser()
    parser.set_output_mode(TemplateParser.OUTPUTMODE_CONSOLE)

    with pytest.raises(ParserError):
        parser.parse('\n'.join(text))


def test_for_loop():
    text = [
        '#: list = ["item 1", "item 2", "item 2"]',
        '#: for item in list',
        'Found $item',
        '#: endfor'
    ]

    parser = TemplateParser()
    parser.set_output_mode(TemplateParser.OUTPUTMODE_CONSOLE)
    result = parser.parse('\n'.join(text))
    assert ['Found item 1', 'Found item 2', 'Found item 2'] == result


def test_for_nested_loop():
    text = [
        '#: list = ["item 1", "item 2", "item 2"]',
        '#: list2 = ["another 1", "another 2"]',
        '#: for item in list',
        'Outer: $item',
        '#: for inner_item in list2',
        'Inner: $inner_item',
        '#: endfor',

        '#: endfor'
    ]

    parser = TemplateParser()
    parser.set_output_mode(TemplateParser.OUTPUTMODE_CONSOLE)
    result = parser.parse('\n'.join(text))
    assert ['Outer: item 1', 'Inner: another 1', 'Inner: another 2', 'Outer: item 2',
            'Inner: another 1', 'Inner: another 2', 'Outer: item 2', 'Inner: another 1',
            'Inner: another 2'] == result


def test_for_empty_list():
    text = [
        '#: list = []',
        '#: for item in list',
        'Found $item',
        '#: endfor'
    ]

    parser = TemplateParser()
    parser.set_output_mode(TemplateParser.OUTPUTMODE_CONSOLE)
    result = parser.parse('\n'.join(text))
    assert [] == result


def test_for_empty_list_with_nested_if():
    text = [
        '#::',
        'list = []',
        'for item in list',
        'if item == "hello"',
        'echo(item)',
        'endif',
        'endfor',
        '#::'
    ]

    parser = TemplateParser()
    parser.set_output_mode(TemplateParser.OUTPUTMODE_CONSOLE)
    result = parser.parse('\n'.join(text))
    assert [] == result
