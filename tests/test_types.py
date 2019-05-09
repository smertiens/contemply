#
# Contemply - A code generator that creates boilerplate files from templates
#
# Copyright (C) 2019  Sean Mertiens
# For more information on licensing see LICENSE file
#
from contemply.parser import *


def test_list_index():
    parser = TemplateParser()
    parser.set_output_mode(TemplateParser.OUTPUTMODE_CONSOLE)
    result = parser.parse("#: list = ['item 1']\n#: echo(list[0])")


def test_list_add():
    parser = TemplateParser()
    parser.set_output_mode(TemplateParser.OUTPUTMODE_CONSOLE)
    result = parser.parse("#: list = ['item 1']\n#: list += 'item 2'")

    assert parser.get_template_context().get('list') == ['item 1', 'item 2']
