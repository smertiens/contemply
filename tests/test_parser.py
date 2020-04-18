from contemply.parser import Parser
from contemply import cli
from contemply import samples
import os

def test_inst():
    ip = Parser()
    assert type(ip) == Parser


def test_assign(monkeypatch):
    text = '\n'.join([
        '--- Contemply',
        'Output is "@console"'
        'This line should just be output.',
        'varname: "What is your name?"',
        'varname2: "What is your second name?"',
        'this should be: ignored',
        'another_var = "Foo"',
        'yet_another_var = "Bar"',
        '---',
        'The password is § another_var § § yet_another_var §!'
    ])

    monkeypatch.setattr(cli, 'user_input', lambda t: 'Foo')

    ip = Parser()
    ip.parse_string(text)
    ip.run()

    assert len(ip.interpreter.processed_templates) == 1
    assert ip.interpreter.processed_templates[0].content == [
        'The password is Foo Bar!'
    ]


def test_ask(monkeypatch, capsys):
    text = '\n'.join([
        '--- Contemply',
        'Output is "@console"',
        'varname: "What is your name?"',
        '---',
        'My name is § varname § Griffin!'
    ])

    monkeypatch.setattr(cli, 'user_input', lambda t: 'Peter')

    ip = Parser()
    ip.parse_string(text)
    ip.run()

    assert len(ip.interpreter.processed_templates) == 1
    assert ip.interpreter.processed_templates[0].content == [
        'My name is Peter Griffin!'
    ]


def test_choose(monkeypatch):
    text = '\n'.join([
        '--- Contemply',
        'Output is "@console"',
        'This line should just be output.',
        'varname: "Choose one!"',
        '   - Monkey',
        '   - Flamingo',
        '   - Llama',
        '---',
        'My favourite animal is the §varname§!'
    ])

    monkeypatch.setattr(cli, 'user_input', lambda t: '2')

    ip = Parser()
    ip.parse_string(text)
    ip.run()

    assert len(ip.interpreter.processed_templates) == 1
    assert ip.interpreter.processed_templates[0].content == [
        'My favourite animal is the Flamingo!'
    ]


def test_echo(capsys):
    text = '\n'.join([
        '--- Contemply',
        'Output is "@null"',
        'This line should just be output.',
        'This one as well.',
        '---'
    ])

    ip = Parser()
    ip.parse_string(text)
    ip.run()

    assert 'This line should just be output.\nThis one as well.\n' in capsys.readouterr()


def test_collect_and_loop(monkeypatch):
    text = '\n'.join([
        '--- Contemply',
        'Output is "@null"',
        'This line should just be output.',
        'varname: "Add some!"',
        '   ...',
        '---',
        'Hello there!',
        'You chose:',
        '... varname -> item',
        ' - § item §',
        '...'
    ])

    monkeypatch.setattr(cli, 'collect', lambda t: [
                        'Item 1', 'Item 2', 'Item 3'])

    ip = Parser()
    ip.parse_string(text)
    ip.run()

    assert len(ip.interpreter.processed_templates) == 1
    assert ip.interpreter.processed_templates[0].content == [
        'Hello there!',
        'You chose:',
        ' - Item 1',
        ' - Item 2',
        ' - Item 3',
    ]

def test_collect_empty_and_loop(monkeypatch):
    text = '\n'.join([
        '--- Contemply',
        'Output is "@null"',
        'This line should just be output.',
        'varname: "Add some!"',
        '   ...',
        '---',
        'Hello there!',
        'You chose:',
        '... varname -> item',
        ' - § item §',
        '...'
    ])

    monkeypatch.setattr(cli, 'collect', lambda t: [])

    ip = Parser()
    ip.parse_string(text)
    ip.run()

    assert len(ip.interpreter.processed_templates) == 1
    assert ip.interpreter.processed_templates[0].content == [
        'Hello there!',
        'You chose:',
    ]


def test_variable_replacement():
    text = '\n'.join([
        '--- Contemply',
        'Output is "@null"',
        'foo = "bar"',
        '---',
        'Hello §foo§!',
        'Hi § foo §!',
        'Ola §  foo         §!',
    ])

    parser = Parser()
    parser.parse_string(text)
    parser.run()

    assert len(parser.interpreter.processed_templates) == 1
    assert parser.interpreter.processed_templates[0].content == ['Hello bar!', 'Hi bar!', 'Ola bar!']


def test_change_markers():
    text = '\n'.join([
        '--- Contemply',
        'Output is "@null"',
        'StartMarker is "$"',
        'EndMarker is "#"',
        'hello = "world"',
        '---',
        'Hello $ hello #!',
    ])

    parser = Parser()
    parser.parse_string(text)
    parser.run()

    assert len(parser.interpreter.processed_templates) == 1
    assert parser.interpreter.processed_templates[0].content == ['Hello world!']
