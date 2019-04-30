#
# Contemply - A code generator that creates boilerplate files from templates
#
# Copyright (C) 2019  Sean Mertiens
# For more information on licensing see LICENSE file
#

from contemply.cpytypes import *


def test_Token():
    token = Token(STRING, 'Hello')
    assert token.value() == 'Hello'
    assert token.type() == STRING


def test_Function():
    args = ['arg1', 121, ['arg2']]
    func = Function('testfunc', args)

    assert func.name() == 'testfunc'
    assert func.args() == args


def test_List():
    data = ['item1', 'item2', 3, 'item4']
    list = List(data)

    assert list.items() == data


def test_VariableAssignment():
    assign = VariableAssignment('myvar', 'Hello World')

    assert assign.varname() == 'myvar'
    assert assign.value() == 'Hello World'


def test_Condition():
    tests = {
        ('yes', '==', 'yes'): True,
        ('yes', '==', 'no'): False,
        (10, '<', 102): True,
        (2534, '>', 213): True,
        (120, '>=', 120): True,
        (120, '>=', 119): True,
        (120, '>=', 189): False,
        (8984, '<=', 10000): True,
        (10000, '<=', 10000): True,
        (10000, '<=', 120): False,
        ('yes', '!=', 'no'): True,
        ('yes', '!=', 'yes'): False,
        (20, '!=', 123): True
    }

    for vals, result in tests.items():
        cond = Condition(vals[0], vals[2], vals[1])
        assert cond.solve() == result, 'Testing {0} {1} {2}'.format(vals[0], vals[1], vals[2])


def test_Block():
    cond = Condition(12, 12, '==')
    block = Block(cond, Block.IF_BLOCK)

    assert block.type() == Block.IF_BLOCK
    assert block.cond() == cond
