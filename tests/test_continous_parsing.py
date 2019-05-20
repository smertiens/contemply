#
# AtraxiCreator - GUI editor for AtraxiFlow scripts
#
# Copyright (C) 2019  Sean Mertiens
# For more information on licensing see LICENSE file
#

from contemply.parser import *


def test_parser_cont():
    text = [
        '#: var1 = "Hello"',
        '#::',
        'echo("hello world")',
        'if var1 == "Hello"',
        'echo("if")',
        'endif',
        '#::'
    ]

    parser = TemplateParser()
    parser.set_output_mode(TemplateParser.OUTPUTMODE_CONSOLE)
    result = parser.parse('\n'.join(text))
    assert result == ['Lorem ipsum', 'adasodk90ßam dpoapdo20ßansd', 'a3ßó=I?Q§)PDJOÖIj0aj90ü9ß3d qd30ßai03d()PQ§R']