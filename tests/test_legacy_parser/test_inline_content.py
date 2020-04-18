#
# Contemply - A code generator that creates boilerplate files from templates
#
# Copyright (C) 2019  Sean Mertiens
# For more information on licensing see LICENSE file
#
import pytest
from contemply import cli
from contemply.exceptions import ParserError
from contemply.interpreter import Interpreter


def test_inline_function(monkeypatch, parser_inst):
    text = [
        "Hello $('Whats your name').",
        'Yummy $("What\'s your favourite food?"). Have some more!'
    ]

    monkeypatch.setattr(cli, 'user_input', lambda t: 'carrots')

    result = parser_inst.parse('\n'.join(text))[Interpreter.DEFAULT_TARGET]
    assert result == ['Hello carrots.', 'Yummy carrots. Have some more!']


def test_inline_function_whitespace(monkeypatch, parser_inst):
    text = [
        "Hello $(   'Whats your name'   ).",
    ]

    monkeypatch.setattr(cli, 'user_input', lambda t: 'carrots')

    result = parser_inst.parse('\n'.join(text))[Interpreter.DEFAULT_TARGET]
    assert result == ['Hello carrots.']

    text = [
        "Hello $ (   'Whats your name'   ).",
    ]

    monkeypatch.setattr(cli, 'user_input', lambda t: 'carrots')

    result = parser_inst.parse('\n'.join(text))[Interpreter.DEFAULT_TARGET]
    assert result == ["Hello $ (   'Whats your name'   )."]


def test_inline_function_syntaxerror(monkeypatch, parser_inst):
    text = [
        "Hello $('Whats your name').",
        'Yummy $("What\'s your fav"ourite food?"). Have some more!'
    ]

    monkeypatch.setattr(cli, 'user_input', lambda t: 'carrots')

    with pytest.raises(ParserError):
        result = parser_inst.parse('\n'.join(text))[Interpreter.DEFAULT_TARGET]


def test_escape_dollarsign(parser_inst):
    text = [
        "#: foo = 'bar'",
        "foo $foo"
    ]

    result = parser_inst.parse('\n'.join(text))[Interpreter.DEFAULT_TARGET]
    assert result == ["foo bar"]

    text[1] = "foo \$foo"

    result = parser_inst.parse('\n'.join(text))[Interpreter.DEFAULT_TARGET]
    assert result == ["foo $foo"]