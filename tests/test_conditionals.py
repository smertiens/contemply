#
# Contemply - A code generator that creates boilerplate files from templates
#
# Copyright (C) 2019-2020  Sean Mertiens
# For more information on licensing see LICENSE file
#

from contemply.parser import Parser
from contemply import cli
from contemply import samples
import os

def test_if_greater_than():
    text = '\n'.join([
        '--- Contemply',
        'Output is "@null"',
        '---',
        '? 5 > 12.5',
        'Wrong',
        '?',
        '? 5 > 2.1',
        'Right',
        '?',
    ])

    parser = Parser()
    parser.parse_string(text)
    parser.run()

    assert len(parser.interpreter.processed_templates) == 1
    assert parser.interpreter.processed_templates[0].content == ['Right']
    
def test_if_greater_than_or_equal():

    text = '\n'.join([
        '--- Contemply',
        'Output is "@null"',
        '---',
        '? 5 > 5',
        'Wrong',
        '?',
        '? 5 >= 5',
        'Right',
        '?',
    ])

    parser = Parser()
    parser.parse_string(text)
    parser.run()

    assert len(parser.interpreter.processed_templates) == 1
    assert parser.interpreter.processed_templates[0].content == ['Right']

def test_if_smaller_than():

    text = '\n'.join([
        '--- Contemply',
        'Output is "@null"',
        '---',
        '? 5 < 2',
        'Wrong',
        '?',
        '? 5 < 8.98',
        'Right',
        '?',
    ])

    parser = Parser()
    parser.parse_string(text)
    parser.run()

    assert len(parser.interpreter.processed_templates) == 1
    assert parser.interpreter.processed_templates[0].content == ['Right']


def test_if_smaller_than_or_equal():

    text = '\n'.join([
        '--- Contemply',
        'Output is "@null"',
        '---',
        '? 239.0 < 239.0',
        'Wrong',
        '?',
        '? 239.0 <= 239.0',
        'Right',
        '?',
    ])

    parser = Parser()
    parser.parse_string(text)
    parser.run()

    assert len(parser.interpreter.processed_templates) == 1
    assert parser.interpreter.processed_templates[0].content == ['Right']

def test_if_with_function():
    text = '\n'.join([
        '--- Contemply',
        'Output is "@null"',
        'foo = "bar"',
        '---',
        '? uppercase(foo) == "BAR"',
        'Hello world!',
        '?'
    ])

    parser = Parser()
    parser.parse_string(text)
    parser.run()

    assert len(parser.interpreter.processed_templates) == 1
    assert parser.interpreter.processed_templates[0].content == ['Hello world!']

def test_if_with_function_inverted():
    text = '\n'.join([
        '--- Contemply',
        'Output is "@null"',
        'foo = "BAR"',
        '---',
        '? "BAR" != lowercase(foo)',
        'Hello world!',
        '?'
    ])

    parser = Parser()
    parser.parse_string(text)
    parser.run()

    assert len(parser.interpreter.processed_templates) == 1
    assert parser.interpreter.processed_templates[0].content == ['Hello world!']


def test_elseif_if_matches():

    text = '\n'.join([
        '--- Contemply',
        'Output is "@null"',
        'foo = "BAR"',
        '---',
        '? foo == "BAR"',
        'Uppercase',
        '?? foo == "bar"',
        'Lowercase',
        '??',
        'Nothing',
        '?'
    ])

    parser = Parser()
    parser.parse_string(text)
    parser.run()

    assert len(parser.interpreter.processed_templates) == 1
    assert parser.interpreter.processed_templates[0].content == ['Uppercase']


def test_elseif_elseif_matches():

    text = '\n'.join([
        '--- Contemply',
        'Output is "@null"',
        'foo = "bar"',
        '---',
        '? foo == "BAR"',
        'Uppercase',
        '?? foo == "bar"',
        'Lowercase',
        '??',
        'Nothing',
        '?'
    ])

    parser = Parser()
    parser.parse_string(text)
    parser.run()

    assert len(parser.interpreter.processed_templates) == 1
    assert parser.interpreter.processed_templates[0].content == ['Lowercase']


def test_elseif_else_matches():

    text = '\n'.join([
        '--- Contemply',
        'Output is "@null"',
        'foo = ""',
        '---',
        '? foo == "BAR"',
        'Uppercase',
        '?? foo == "bar"',
        'Lowercase',
        '??',
        'Nothing',
        '?'
    ])

    parser = Parser()
    parser.parse_string(text)
    parser.run()

    assert len(parser.interpreter.processed_templates) == 1
    assert parser.interpreter.processed_templates[0].content == ['Nothing']
