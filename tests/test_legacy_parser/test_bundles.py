#
# Contemply - A code generator that creates boilerplate files from templates
#
# Copyright (C) 2019  Sean Mertiens
# For more information on licensing see LICENSE file
#
import pytest
from contemply.exceptions import ParserError, BundleException
from contemply.legacy.interpreter import Interpreter


def test_bundle_load(parser_inst):
    text = [
        "#: bar('works')"
    ]

    with pytest.raises(ParserError):
        result = parser_inst.parse('\n'.join(text))[Interpreter.DEFAULT_TARGET]

    parser_inst.load_extension('tests.fixtures.foo_extension')

    result = parser_inst.parse('\n'.join(text))[Interpreter.DEFAULT_TARGET]


def test_bundle_load_error(parser_inst):
    with pytest.raises(BundleException):
        parser_inst.load_extension('tests.fixtures.bar_extension')
