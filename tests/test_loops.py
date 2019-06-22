#
# Contemply - A code generator that creates boilerplate files from templates
#
# Copyright (C) 2019  Sean Mertiens
# For more information on licensing see LICENSE file
#

import pytest
from contemply.frontend import TemplateParser
from contemply.interpreter import *


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
    result = parser.parse('\n'.join(text))[Interpreter.DEFAULT_TARGET]
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
    result = parser.parse('\n'.join(text))[Interpreter.DEFAULT_TARGET]
    assert ['outer: 0', 'inner: 0', 'inner: 1', 'inner: 2', 'outer: 1', 'inner: 0', 'inner: 1',
            'inner: 2', 'outer: 2', 'inner: 0', 'inner: 1', 'inner: 2', 'outer: 3',
            'inner: 0', 'inner: 1', 'inner: 2'] == result


def test_while_loop_break():
    text = [
        '#: num = 0',
        '#: while num <= 5',
        'This run no. $num',
        '#: if num == 3',
        '#: break',
        'This should not be processed',
        '#: endif',
        '#: num = num + 1',
        '#: endwhile'
    ]

    expected = [
        'This run no. 0',
        'This run no. 1',
        'This run no. 2',
        'This run no. 3'
    ]

    parser = TemplateParser()
    parser.set_output_mode(TemplateParser.OUTPUTMODE_CONSOLE)
    result = parser.parse('\n'.join(text))[Interpreter.DEFAULT_TARGET]
    assert result == expected


def test_while_loop_max_runs():
    text = [
        '#: while True',
        '#: endwhile'
    ]

    parser = TemplateParser()
    parser.set_output_mode(TemplateParser.OUTPUTMODE_CONSOLE)

    # check if default value is set correctly
    assert Interpreter.MAX_LOOP_RUNS == 10000

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
    result = parser.parse('\n'.join(text))[Interpreter.DEFAULT_TARGET]
    assert ['Found item 1', 'Found item 2', 'Found item 2'] == result


def test_for_loop_break():
    text = [
        '#: list = ["item 1", "item 2", "item 3"]',
        '#: for item in list',
        'Found $item',
        '#: break',
        '#: endfor'
    ]

    parser = TemplateParser()
    parser.set_output_mode(TemplateParser.OUTPUTMODE_CONSOLE)
    result = parser.parse('\n'.join(text))[Interpreter.DEFAULT_TARGET]
    assert result == ['Found item 1']


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
    result = parser.parse('\n'.join(text))[Interpreter.DEFAULT_TARGET]
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
    result = parser.parse('\n'.join(text))[Interpreter.DEFAULT_TARGET]
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
    result = parser.parse('\n'.join(text))[Interpreter.DEFAULT_TARGET]
    assert [] == result


def test_mixed_nested_loops_break():
    text = [
        '#::',
        'list = ["item 1", "item 2", "item 3"]',
        'for item in list',
        '#::',
        'Hello $item',
        '#: num = 0',
        '#: while True',
        '#: if num == 2',
        '#: break',
        '#: endif',
        'This is number $num',
        '#: num = num + 1',
        '#: endwhile',
        '#: if item == "item 2"',
        '#: break',
        '#: endif',
        '#: endfor',
    ]

    parser = TemplateParser()
    parser.set_output_mode(TemplateParser.OUTPUTMODE_CONSOLE)
    result = parser.parse('\n'.join(text))[Interpreter.DEFAULT_TARGET]
    assert ['Hello item 1', 'This is number 0', 'This is number 1', 'Hello item 2', 'This is number 0',
            'This is number 1'] == result


def test_wrong_break():
    text = [
        '#::',
        'list = []',
        'break',
        '#::'
    ]

    parser = TemplateParser()
    parser.set_output_mode(TemplateParser.OUTPUTMODE_CONSOLE)

    with pytest.raises(ParserError):
        # Unexpected break
        result = parser.parse('\n'.join(text))
