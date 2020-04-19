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

def test_single_line_call(capsys):
    text = '\n'.join([
        '--- Contemply',
        'Output is "@null"',
        '! echo("Hello World")',
        '---',
        '! echo("Foo Bar")'
    ])

    parser = Parser()
    parser.parse_string(text)
    parser.run()

    assert len(parser.interpreter.processed_templates) == 1
    assert 'Hello World\nFoo Bar\n' in capsys.readouterr()


def test_assign_function_result():
    text = '\n'.join([
        '--- Contemply',
        'Output is "@null"',
        'test = uppercase("hello")',
        '---',
        '§ test §'
    ])

    parser = Parser()
    parser.parse_string(text)
    parser.run()

    assert len(parser.interpreter.processed_templates) == 1
    assert parser.interpreter.processed_templates[0].content == ['HELLO']

def test_function_arguments():

    class TestMod:

        def testFunc(self, args):
            assert args == [12, 394.033, "hello", "world"]
            return "{} {} {} {}".format(args[0], args[1], args[2], args[3])

    text = '\n'.join([
        '--- Contemply',
        'Output is "@null"',
        'test = testFunc(12, 394.033, "hello", "world")',
        '---',
        '§ test §'
    ])

    mod = TestMod()

    parser = Parser()
    parser.env.function_lookups.append(mod)
    parser.interpreter.load_env()
    parser.parse_string(text)
    parser.run()

    assert len(parser.interpreter.processed_templates) == 1
    assert parser.interpreter.processed_templates[0].content == ['12 394.033 hello world']

################################
# String functions
################################

def test_str_lowercase():
    text = '\n'.join([
        '--- Contemply',
        'Output is "@null"',
        'test = lowercase("HELLO")',
        '---',
        '§ test §'
    ])

    parser = Parser()
    parser.parse_string(text)
    parser.run()

    assert len(parser.interpreter.processed_templates) == 1
    assert parser.interpreter.processed_templates[0].content == ['hello']


def test_str_capitalize():
    text = '\n'.join([
        '--- Contemply',
        'Output is "@null"',
        'test = capitalize("hello")',
        '---',
        '§ test §'
    ])

    parser = Parser()
    parser.parse_string(text)
    parser.run()

    assert len(parser.interpreter.processed_templates) == 1
    assert parser.interpreter.processed_templates[0].content == ['Hello']


def test_str_contains():
    text = '\n'.join([
        '--- Contemply',
        'Output is "@null"',
        'test = contains("hello", "ell")',
        '---',
        '§ test §'
    ])

    parser = Parser()
    parser.parse_string(text)
    parser.run()

    assert len(parser.interpreter.processed_templates) == 1
    assert parser.interpreter.processed_templates[0].content == ['True']

def test_str_replace():
    text = '\n'.join([
        '--- Contemply',
        'Output is "@null"',
        'test = replace("hello world", "world", "foo")',
        '---',
        '§ test §'
    ])

    parser = Parser()
    parser.parse_string(text)
    parser.run()

    assert len(parser.interpreter.processed_templates) == 1
    assert parser.interpreter.processed_templates[0].content == ['hello foo']