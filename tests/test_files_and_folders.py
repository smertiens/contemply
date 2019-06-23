#
# Contemply - A code generator that creates boilerplate files from templates
#
# Copyright (C) 2019  Sean Mertiens
# For more information on licensing see LICENSE file
#
from contemply.interpreter import Interpreter
import os, platform

# checking file permissions:
# https://stackoverflow.com/questions/5337070/how-can-i-get-a-files-permission-mask

def test_make_folders_default(tmpdir, monkeypatch, parser_inst):
    tmpdir = str(tmpdir)
    checkpath1 = os.path.join(tmpdir, 'foo', 'bar')
    checkpath2 = os.path.join(tmpdir, 'foo', 'bar', 'hello')

    text = [
        "#: var1 = 'hello'",
        "#: makeFolders('foo/bar')",
        "#: makeFolders('foo/bar/$var1')"
    ]

    assert not os.path.exists(checkpath1)
    assert not os.path.exists(checkpath2)

    monkeypatch.setattr(os, 'getcwd', lambda: tmpdir)
    result = parser_inst.parse('\n'.join(text))[Interpreter.DEFAULT_TARGET]

    assert os.path.exists(checkpath1)
    assert os.path.exists(checkpath2)


def test_make_folders_chmod(tmpdir, monkeypatch, parser_inst):
    if  'TRAVIS_TEST' in os.environ:
        return

    tmpdir = str(tmpdir)
    checkpath = os.path.join(tmpdir, 'foo', 'bar')

    text = [
        "#: makeFolders('foo/bar', '644')"
    ]

    assert not os.path.exists(os.path.join(tmpdir, 'foo', 'bar'))
    monkeypatch.setattr(os, 'getcwd', lambda: tmpdir)
    result = parser_inst.parse('\n'.join(text))[Interpreter.DEFAULT_TARGET]
    assert os.path.exists(checkpath)

    # this raises a PermissionError if run on Travis with Python < 3.7
    if platform.system() != 'Windows':
        st = os.stat(checkpath)
        perm = oct(st.st_mode  & 0o777)
        assert perm == '0o644'