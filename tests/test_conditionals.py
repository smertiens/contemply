from contemply.frontend import TemplateParser
from contemply.interpreter import Interpreter

def test_if_conditions():
    parser = TemplateParser()
    parser.set_output_mode(TemplateParser.OUTPUTMODE_CONSOLE)

    text = [
        '#: var1 = "World"',
        '#: var2 = "demo"',
        '#: if var1 == "Hello"',
        'if block',
        '#: elseif var1 == "World"',
        'first elseif',
        '#: elseif var1 == "World2"',
        'second elseif',
        '#: else',
        'else block',
        '#: if var2 == "demo"',
        'inner if',
        '#: endif',
        '#: endif'
    ]

    result = parser.parse('\n'.join(text))[Interpreter.DEFAULT_TARGET]
    assert result == ['first elseif']

    text[0] = '#: var1 = "World2"'
    result = parser.parse('\n'.join(text))[Interpreter.DEFAULT_TARGET]
    assert result == ['second elseif']

    text[0] = '#: var1 = "World3"'
    result = parser.parse('\n'.join(text))[Interpreter.DEFAULT_TARGET]
    assert result == ['else block', 'inner if']

    text[1] ='#: var2 = "no demo"'
    result = parser.parse('\n'.join(text))[Interpreter.DEFAULT_TARGET]
    assert result == ['else block']

def test_parser_if():
    text = [
        '#: var1 = "Hello"',
        '#: var2 = "Hello"',
        '#: if var1 == var2',
        'Lorem ipsum',
        'or something',
        '#: endif'
    ]

    parser = TemplateParser()
    parser.set_output_mode(TemplateParser.OUTPUTMODE_CONSOLE)
    result = parser.parse('\n'.join(text))[Interpreter.DEFAULT_TARGET]
    assert result == ['Lorem ipsum', 'or something']

    text[0] = '#: var1 = "Not Hello"'

    result = parser.parse('\n'.join(text))[Interpreter.DEFAULT_TARGET]
    assert result == []


def test_parser_if_else():
    text = [
        '#: var1 = "Hello"',
        '#: var2 = "Not Hello"',
        '#: if var1 == var2',
        'Lorem ipsum',
        '#: else',
        'or something',
        '#: endif'
    ]

    parser = TemplateParser()
    parser.set_output_mode(TemplateParser.OUTPUTMODE_CONSOLE)
    result = parser.parse('\n'.join(text))[Interpreter.DEFAULT_TARGET]
    assert result == ['or something']

    text[0] = '#: var1 = "Not Hello"'
    result = parser.parse('\n'.join(text))[Interpreter.DEFAULT_TARGET]
    assert result == ['Lorem ipsum']
