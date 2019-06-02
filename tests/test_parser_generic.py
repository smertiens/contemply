#
# Contemply - A code generator that creates boilerplate files from templates
#
# Copyright (C) 2019  Sean Mertiens
# For more information on licensing see LICENSE file
#

from contemply.parser import *
import pytest

def test_parser_simple():
    text = '#: var1 = "Hello"\n#: var2 = "World"\n$var1 $var2'
    parser = TemplateParser()
    parser.set_output_mode(TemplateParser.OUTPUTMODE_CONSOLE)
    result = parser.parse(text)

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
    result = parser.parse('\n'.join(text))
    assert result == ['Lorem ipsum', '# Comment']
    assert not parser.get_template_context().has('var1')


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
    result = parser.parse('\n'.join(text))
    assert result == ['Hello']

    text[2] = '#: test3 = 5'

    parser = TemplateParser()
    parser.set_output_mode(TemplateParser.OUTPUTMODE_CONSOLE)
    result = parser.parse('\n'.join(text))
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
    result = parser.parse('\n'.join(text))
    assert result == ['a p38 (P=)(§RZ=Pru ÄÖ\'Ö§Ü§§"U304 2Q§3"kljkL"','::;_;_:;!"§%&/()=?adklköölkk>><<<']

def test_set_output(tmpdir):
    tmpdir = str(tmpdir)
    testfile = tmpdir + '/' + 'demo.pytpl'

    # create a demo file
    with open(testfile, 'w') as f:
        f.write('\n'.join([
            '#: echo("Hello World!")',
            '#: setOutput("./demo.txt")',
            'Contentline'
        ]))

    assert not os.path.exists('./demo.txt')

    parser = TemplateParser()
    result = parser.parse_file(testfile)
    assert result == ['Contentline']

    assert os.path.exists('./demo.txt')

    with open('./demo.txt', 'r') as f:
        assert f.read() == 'Contentline'

    os.unlink('./demo.txt')
    assert not os.path.exists('./demo.txt')

def test_access_illegal_path(tmpdir):
    tmpdir = str(tmpdir)
    testfile = tmpdir + '/' + 'demo.pytpl'
    outfile = tmpdir + '/' + 'demo.txt'

    # create a demo file
    with open(testfile, 'w') as f:
        f.write('\n'.join([
            '#: echo("Hello World!")',
            '#: setOutput("%s")' % (outfile),
            'Contentline'
        ]))

    assert not os.path.exists(outfile)
    parser = TemplateParser()

    with pytest.raises(SecurityException):
        result = parser.parse_file(testfile)
        assert result == ['Contentline']

    assert not os.path.exists(outfile)