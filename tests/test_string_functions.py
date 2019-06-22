#
# Contemply - A code generator that creates boilerplate files from templates
#
# Copyright (C) 2019  Sean Mertiens
# For more information on licensing see LICENSE file
#
import pytest
from contemply.frontend import TemplateParser


def test_uppercase():
    parser = TemplateParser()
    parser.set_output_mode(TemplateParser.OUTPUTMODE_CONSOLE)
    parser.parse("#::\nmy_str = 'Hello World'\nmy_str_upper = uppercase(my_str)")

    assert parser.get_template_context().get('my_str') == 'Hello World'
    assert parser.get_template_context().get('my_str_upper') == 'HELLO WORLD'


def test_lowercase():
    parser = TemplateParser()
    parser.set_output_mode(TemplateParser.OUTPUTMODE_CONSOLE)
    parser.parse("#::\nmy_str = 'Hello World'\nmy_str_upper = lowercase(my_str)")

    assert parser.get_template_context().get('my_str') == 'Hello World'
    assert parser.get_template_context().get('my_str_upper') == 'hello world'


def test_contains():
    parser = TemplateParser()
    parser.set_output_mode(TemplateParser.OUTPUTMODE_CONSOLE)
    parser.parse('\n'.join([
        '#::',
        'check1 = contains("The quick brown fox!", "fox")',
        'check2 = contains("The quick brown fox!", "eagle")',
        'check3 = contains("The quick brown fox!", "quick")',
        'check4 = contains("The quick brown fox!", "the")'
    ]))

    assert parser.get_template_context().get('check1')
    assert not parser.get_template_context().get('check2')
    assert parser.get_template_context().get('check3')
    assert not parser.get_template_context().get('check4')


def test_capitalize():
    parser = TemplateParser()
    parser.set_output_mode(TemplateParser.OUTPUTMODE_CONSOLE)
    parser.parse("#::\nmy_str = 'hello world'\nmy_str_upper = capitalize(my_str)")

    assert parser.get_template_context().get('my_str') == 'hello world'
    assert parser.get_template_context().get('my_str_upper') == 'Hello world'


def test_replace():
    parser = TemplateParser()
    parser.set_output_mode(TemplateParser.OUTPUTMODE_CONSOLE)
    parser.parse("#::\nmy_str = 'Hello World'\nmy_str_replace = replace(my_str, 'World', 'Mars!')")

    assert parser.get_template_context().get('my_str') == 'Hello World'
    assert parser.get_template_context().get('my_str_replace') == 'Hello Mars!'


def test_replace_multiple(parser_inst):
    parser_inst.parse("#::\nmy_str = 'Hello World'\nmy_str_replace = replace(my_str, ['e', 'o'], '!')")

    assert parser_inst.get_template_context().get('my_str') == 'Hello World'
    assert parser_inst.get_template_context().get('my_str_replace') == 'H!ll! W!rld'


def test_size():
    parser = TemplateParser()
    parser.set_output_mode(TemplateParser.OUTPUTMODE_CONSOLE)
    parser.parse("#::\nmy_str = 'Hello World'\nlen = size(my_str)")

    assert parser.get_template_context().get('my_str') == 'Hello World'
    assert parser.get_template_context().get('len') == 11
