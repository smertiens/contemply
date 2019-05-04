#
# AtraxiCreator - GUI editor for AtraxiFlow scripts
#
# Copyright (C) 2019  Sean Mertiens
# For more information on licensing see LICENSE file
#

from contemply.parser import *
import pytest


def test_VariableAssignment():
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

    with pytest.raises(KeyError):
        ctx.get('not_Existing')


def test_VariableReplacement():
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
        assert not ctx.process_variables('$myvarinanotherword and another on') == 'Hello Worldinanotherword and another one'