from contemply.simple_parser import Parser, SectionContext
from contemply import cli
from contemply import samples
import os

def test_inst():
    ip = Parser()
    assert type(ip) == Parser


def test_assign(monkeypatch):
    text = '\n'.join([
        '--- Contemply',
        'This line should just be output.',
        'varname: What is your name?',
        'varname2: What is your second name?',
        'this should be: ignored',
        'another_var = Foo',
        'yet_another_var = Bar',
        '---',
        'asd'
    ])

    monkeypatch.setattr(cli, 'user_input', lambda t: 'Peter')

    ip = Parser()
    r = ip.parse_string(text)
    assert isinstance(ip._ctx, SectionContext)

    assert ip._ctx.data == {
        'varname': 'Peter',
        'varname2': 'Peter',
        'another_var': 'Foo',
        'yet_another_var': 'Bar',
    }


def test_ask(monkeypatch, capsys):
    text = '\n'.join([
        '--- Contemply',
        'This line should just be output.',
        'varname: What is your name?',
        '---'
    ])

    monkeypatch.setattr(cli, 'user_input', lambda t: 'Peter')

    ip = Parser()
    r = ip.parse_string(text)
    assert isinstance(ip._ctx, SectionContext)

    assert ip._ctx.data == {'varname': 'Peter'}


def test_choose(monkeypatch):
    text = '\n'.join([
        '--- Contemply',
        'This line should just be output.',
        'varname: Choose one!',
        '   - Monkey',
        '\t- Flamingo',
        '\t- Llama',
        '---'
    ])

    monkeypatch.setattr(cli, 'user_input', lambda t: '2')

    ip = Parser()
    r = ip.parse_string(text)
    assert isinstance(ip._ctx, SectionContext)

    assert ip._ctx.data == {'varname': 'Flamingo'}


def test_echo(capsys):
    text = '\n'.join([
        '--- Contemply',
        'This line should just be output.',
        'This one as well.',
        '---'
    ])

    ip = Parser()
    ip.parse_string(text)

    assert 'This line should just be output.\nThis one as well.\n' in capsys.readouterr()


def test_internal_assignment():
    text = '\n'.join([
        '--- Contemply',
        'StartMarker is Foo Bar',
        '---'
    ])

    ip = Parser()
    ctx = SectionContext()
    r = ip.parse_string(text)
    assert isinstance(ip._ctx, SectionContext)
    
    s = ctx.settings
    s['StartMarker'] = 'Foo Bar'

    assert ip._ctx.settings == s


def test_collect(monkeypatch):
    text = '\n'.join([
        '--- Contemply',
        'This line should just be output.',
        'varname: Add some!',
        '   ...',
        '---'
    ])

    monkeypatch.setattr(cli, 'collect', lambda t: [
                        'Item 1', 'Item 2', 'Item 3'])

    ip = Parser()
    r = ip.parse_string(text)
    assert isinstance(ip._ctx, SectionContext)

    assert ip._ctx.data == {'varname': ['Item 1', 'Item 2', 'Item 3']}


def test_variable_replacement():
    text = '\n'.join([
        '--- Contemply',
        'foo = bar',
        'hello = world',
        '---',
        'Hello § hello §!',
        'Foo § foo §!'
    ])

    parser = Parser()
    parser.parse_string(text)

    assert parser._ctx.output == ['Hello world!', 'Foo bar!']


def test_change_markers():
    text = '\n'.join([
        '--- Contemply',
        'StartMarker is $',
        'EndMarker is #',
        'hello = world',
        '---',
        'Hello $ hello #!',
    ])

    parser = Parser()
    parser.parse_string(text)

    assert parser._ctx.output == ['Hello world!']
