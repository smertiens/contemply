#
# AtraxiCreator - GUI editor for AtraxiFlow scripts
#
# Copyright (C) 2019  Sean Mertiens
# For more information on licensing see LICENSE file
#

from contemply.tokenizer import *
from contemply.parser import TemplateContext


def test_token_detection():
    text = '#: demo = "Hello World"\necho("Function call")\n#: var = ["item1", "item2"]'.split('\n')
    expected = [CMD_LINE_START, SYMBOL, ASSIGN, STRING, SYMBOL, LPAR, STRING, RPAR,
                CMD_LINE_START, SYMBOL, ASSIGN, LSQRBR, STRING, COMMA, STRING, RSQRBR]

    actual = []

    ctx = TemplateContext()
    ctx.set_text(text)
    t = Tokenizer(ctx)

    for i, line in enumerate(text):
        ctx.set_position(i, 0)
        t.update_position()
        token = t.get_next_token()
        while token.type() != EOF:
            actual.append(token.type())
            token = t.get_next_token()

    assert actual == expected
