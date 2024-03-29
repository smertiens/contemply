#
# Contemply - A code generator that creates boilerplate files from templates
#
# Copyright (C) 2019  Sean Mertiens
# For more information on licensing see LICENSE file
#

from contemply.frontend import TemplateParser
from contemply.interpreter import Interpreter
from contemply.exceptions import *
from contemply import cli
from colorama import Fore
import pytest, os


def test_parser_simple():
    text = '#: var1 = "Hello"\n#: var2 = "World"\n$var1 $var2'
    parser = TemplateParser()
    parser.set_output_mode(TemplateParser.OUTPUTMODE_CONSOLE)
    result = parser.parse(text)[Interpreter.DEFAULT_TARGET]

    assert result == ['Hello World']
    assert parser.get_template_context().get('var1') == 'Hello'
    assert parser.get_template_context().get('var2') == 'World'


def test_parser_skip_comments():
    text = [
        '#% var1 = "Hello"',
        'Lorem ipsum',
        '# Comment'
    ]

    parser = TemplateParser()
    parser.set_output_mode(TemplateParser.OUTPUTMODE_CONSOLE)
    result = parser.parse('\n'.join(text))[Interpreter.DEFAULT_TARGET]
    assert result == ['Lorem ipsum', '# Comment']
    assert not parser.get_template_context().has('var1')


def test_parser_indented_comment_in_commandlbock(parser_inst):
    text = [
        '#::',
        '\t#% This is a comment',
        '#::',
        'Lorem ipsum'
    ]

    result = parser_inst.parse('\n'.join(text))[Interpreter.DEFAULT_TARGET]
    assert result == ['Lorem ipsum']


def test_simple_expressions():
    text = [
        '#: test1 = 10',
        '#: test2 = 8',
        '#: test3 = 18',
        '#: result = 10 + 8',
        '#: if test3 == result',
        'Hello',
        '#: endif'
    ]

    parser = TemplateParser()
    parser.set_output_mode(TemplateParser.OUTPUTMODE_CONSOLE)
    result = parser.parse('\n'.join(text))[Interpreter.DEFAULT_TARGET]
    assert result == ['Hello']

    text[2] = '#: test3 = 5'

    parser = TemplateParser()
    parser.set_output_mode(TemplateParser.OUTPUTMODE_CONSOLE)
    result = parser.parse('\n'.join(text))[Interpreter.DEFAULT_TARGET]
    assert result == []


def test_parser_process_special_chars():
    text = [
        '#: var1 = "Hello"',
        '#: if var1 == "Hello"',
        'a p38 (P=)(§RZ=Pru ÄÖ\'Ö§Ü§§"U304 2Q§3"kljkL"',
        '::;_;_:;!"§%&/()=?adklköölkk>><<<',
        '#: endif'
    ]

    parser = TemplateParser()
    parser.set_output_mode(TemplateParser.OUTPUTMODE_CONSOLE)
    result = parser.parse('\n'.join(text))[Interpreter.DEFAULT_TARGET]
    assert result == ['a p38 (P=)(§RZ=Pru ÄÖ\'Ö§Ü§§"U304 2Q§3"kljkL"', '::;_;_:;!"§%&/()=?adklköölkk>><<<']


def test_set_output(tmpdir, capsys, parser_inst):
    tmpdir = str(tmpdir)
    testfile = tmpdir + '/' + 'demo.pytpl'

    # create a demo file
    with open(testfile, 'w') as f:
        f.write('\n'.join([
            '#: setOutput("./demo.txt")'
        ]))

    #parser_inst.set_output_mode(TemplateParser.OUTPUTMODE_FILE)
    result = parser_inst.parse_file(testfile)

    assert 'This function is deprecated and WILL NOT work. See ' + \
            '"Creating multiple files" in the docs' in capsys.readouterr().out


def test_access_illegal_path(tmpdir, monkeypatch):
    tmpdir = str(tmpdir)
    testfile = tmpdir + '/' + 'demo.pytpl'
    outfile = '/../../demo.txt'

    monkeypatch.setattr(os, 'getcwd', lambda: tmpdir)

    # create a demo file
    with open(testfile, 'w') as f:
        f.write('\n'.join([
            '#: echo("Hello World!")',
            '#: >> "%s"' % (outfile),
            'Contentline'
        ]))

    assert not os.path.exists(outfile)
    parser = TemplateParser()

    with pytest.raises(SecurityException):
        result = parser.parse_file(testfile)[Interpreter.DEFAULT_TARGET]
        assert result == ['Contentline']

    assert not os.path.exists(outfile)


def test_mutlifile_output(monkeypatch, parser_inst, tmpdir):
    tmpdir = str(tmpdir)
    file1 = os.path.join(tmpdir, 'hello.txt')
    file2 = os.path.join(tmpdir, 'foo', 'bar', 'demo.txt')

    text = [
        '#: >> "hello.txt"',
        'Hello World',
        'Just testing.',
        '#: >> "/foo/bar/demo.txt", True',
        'This is a demo',
        '#: <<'
    ]

    assert not os.path.exists(file1)
    assert not os.path.exists(file2)

    monkeypatch.setattr(os, 'getcwd', lambda: tmpdir)
    parser_inst.set_output_mode(TemplateParser.OUTPUTMODE_FILE)
    result = parser_inst.parse('\n'.join(text))

    assert 'hello.txt' in result
    assert '/foo/bar/demo.txt' in result

    assert os.path.exists(file1)
    assert os.path.exists(file2)


def test_multifile_output_prompt_default(tmpdir, parser_inst, monkeypatch):
    tmpdir = str(tmpdir)
    file1 = os.path.join(tmpdir, 'hello.txt')
    file2 = os.path.join(tmpdir, 'main_output.txt')

    text = [
        '#: name = "Peter"',
        'Hello $name',
        'Just testing.',
        '#: >> "hello.txt"',
        'This is a demo',
        '#: <<'
    ]

    assert not os.path.exists(file1)
    assert not os.path.exists(file2)

    monkeypatch.setattr(os, 'getcwd', lambda: tmpdir)
    monkeypatch.setattr(cli, 'user_input', lambda t: 'main_output.txt')
    parser_inst.set_output_mode(TemplateParser.OUTPUTMODE_FILE)
    result = parser_inst.parse('\n'.join(text))

    assert 'hello.txt' in result
    assert Interpreter.DEFAULT_TARGET in result

    assert os.path.exists(file1)
    assert os.path.exists(file2)

    with open(file1) as f:
        assert f.read() == 'This is a demo'

    with open(file2) as f:
        assert f.read() == 'Hello Peter\nJust testing.'


def test_add_function_lookup(parser_inst):
    from contemply.samples import function_extension

    text = [
        '#: res = my_function()',
        'I say $res',
        '#: if True == Yes',
        'Builtins are also imported',
        '#: endif'
    ]

    parser_inst.register_lookup_module(function_extension)
    result = parser_inst.parse('\n'.join(text))[Interpreter.DEFAULT_TARGET]

    assert result == ['I say Hello world!', 'Builtins are also imported']


def test_output_jnside_commandblock(parser_inst):
    text = [
        '#::',
        'var1 = "World"',
        'var2 = "bar"',
        '>> "demo.txt"',
        'output("Hello $var1")',
        '<<',
        '',
        '>> "demo2.txt"',
        '-> "Foo $var2"',
        '<<',
        '#::'
    ]

    result = parser_inst.parse('\n'.join(text))

    assert result['demo.txt'] == ['Hello World']
    assert result['demo2.txt'] == ['Foo bar']
