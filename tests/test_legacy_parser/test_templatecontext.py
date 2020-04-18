#
# Contemply - A code generator that creates boilerplate files from templates
#
# Copyright (C) 2019  Sean Mertiens
# For more information on licensing see LICENSE file
#

from contemply.legacy.parser import *
import pytest


def test_variable_assignment():
    data = {
        'var1': 23,
        'var2': 'hello',
        'var3': True,
    }

    ctx = TemplateContext()

    for d, r in data.items():
        ctx.set(d, r)
        assert ctx.has(d)
        assert ctx.get(d) == r

    assert not ctx.has('something_else')

    with pytest.raises(ParserError):
        ctx.get('not_Existing')


def test_variable_replacement():
    ctx = TemplateContext()

    ctx.set('myvar', 'Hello World')
    ctx.set('myvartwo', 25)
    ctx.set('anotherone', 'table')

    assert ctx.process_variables('$myvar') == 'Hello World'
    assert ctx.process_variables('$myvartwo') == str(25)
    assert ctx.process_variables('$anotherone') == 'table'

    assert ctx.process_variables(
        'This is $myvar and we have $myvartwo monkeys on the $anotherone!') == 'This is Hello World and we have 25 monkeys on the table!'

    with pytest.raises(ParserError):
        assert not ctx.process_variables(
            '$myvarinanotherword and another on') == 'Hello Worldinanotherword and another one'


def test_listvar():
    ctx = TemplateContext()

    ctx.set('myvar', ['item 1', 'item 2'])
    assert ctx.process_variables('$myvar[0]') == 'item 1'
    assert ctx.process_variables('$myvar[1]') == 'item 2'
    assert ctx.process_variables('$myvar') == "['item 1', 'item 2']"
