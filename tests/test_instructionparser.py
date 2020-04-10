from contemply.instruction_parser import InstructionParser
from contemply import cli


def test_inst():
    ip = InstructionParser()
    assert type(ip) == InstructionParser


def test_assign(monkeypatch):
    text = '\n'.join([
        'This line should just be output.',
        'varname: What is your name?',
        'varname2: What is your second name?',
        'this should be: ignored',
        'another_var = Foo',
        'yet_another_var = Bar',
    ])

    monkeypatch.setattr(cli, 'user_input', lambda t: 'Peter')

    ip = InstructionParser()
    r = ip.parse(text)

    assert r == {
        'varname': 'Peter',
        'varname2': 'Peter',
        'another_var': 'Foo',
        'yet_another_var': 'Bar',
    }


def test_ask(monkeypatch, capsys):
    text = '\n'.join([
        'This line should just be output.',
        'varname: What is your name?'
    ])

    monkeypatch.setattr(cli, 'user_input', lambda t: 'Peter')

    ip = InstructionParser()
    r = ip.parse(text)

    assert r == {'varname': 'Peter'}


def test_choose(monkeypatch):
    text = '\n'.join([
        'This line should just be output.',
        'varname: Choose one!',
        '   - Monkey',
        '\t- Flamingo',
        '\t- Llama'
    ])

    monkeypatch.setattr(cli, 'user_input', lambda t: '2')

    ip = InstructionParser()
    r = ip.parse(text)

    assert r == {'varname': 'Flamingo'}


def test_echo(capsys):
    text = '\n'.join([
        'This line should just be output.',
        'This one as well.'
    ])

    ip = InstructionParser()
    ip.parse(text)

    assert text + '\n' in capsys.readouterr()


def test_internal_assignment():
    text = '\n'.join([
        'Output is Foo Bar'
    ])

    ip = InstructionParser()
    r = ip.parse(text)

    s = ip.settings
    s['Output'] = 'Foo Bar'

    assert ip.settings == s


def test_collect(monkeypatch):
    text = '\n'.join([
        'This line should just be output.',
        'varname: Add some!',
        '   ...'
    ])

    monkeypatch.setattr(cli, 'collect', lambda t: [
                        'Item 1', 'Item 2', 'Item 3'])

    ip = InstructionParser()
    r = ip.parse(text)

    assert r == {'varname': ['Item 1', 'Item 2', 'Item 3']}
