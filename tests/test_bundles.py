#
# Contemply - A code generator that creates boilerplate files from templates
#
# Copyright (C) 2019-2020  Sean Mertiens
# For more information on licensing see LICENSE file
#
import pytest
from contemply.exceptions import BundleException
from contemply.parser import Parser, ParserException

def test_bundle_load(capsys):

    text = '\n'.join([
        '--- Contemply',
        'Output is "@null"',
        '! newstyle_bar("is working")',
        '---',
    ])

    parser = Parser()
    parser.env.load_extension("tests.fixtures.foo_extension")
    parser.interpreter.load_env()
    parser.parse_string(text)
    parser.run()

    assert len(parser.interpreter.processed_templates) == 1
    assert 'This is working!\n' in capsys.readouterr()

def test_bundle_load_error(parser_inst):
    with pytest.raises(BundleException):
        parser_inst.load_extension('tests.fixtures.bar_extension')
