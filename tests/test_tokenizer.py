#
# Contemply - A code generator that creates boilerplate files from templates
#
# Copyright (C) 2019  Sean Mertiens
# For more information on licensing see LICENSE file
#

from contemply.tokenizer import *
from contemply.parser import TemplateContext


def test_token_detection():
    text = '#: demo = "Hello World"\necho("Function call")\n#: var = ["item1", "item2"]'
    expected = [CMD_LINE_START, SYMBOL, ASSIGN, STRING, NEWLINE, SYMBOL, LPAR, STRING, RPAR, NEWLINE,
                CMD_LINE_START, SYMBOL, ASSIGN, LSQRBR, STRING, COMMA, STRING, RSQRBR]

    actual = []

    ctx = TemplateContext()
    ctx.set_text(text)
    t = Tokenizer(ctx)

    token = t.get_next_token()

    while token.type() != EOF:
        actual.append(token.type())
        token = t.get_next_token()

    assert actual == expected

