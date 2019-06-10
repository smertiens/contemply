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
    checkpath = os.path.join(tmpdir, 'foo', 'bar')

    text = [
        "#: makeFolders('foo/bar')"
    ]

    assert not os.path.exists(os.path.join(tmpdir, 'foo', 'bar'))
    monkeypatch.setattr(os, 'getcwd', lambda: tmpdir)
    result = parser_inst.parse('\n'.join(text))[Interpreter.DEFAULT_TARGET]
    assert os.path.exists(checkpath)


def test_make_folders_chmod(tmpdir, monkeypatch, parser_inst):
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
    if platform.system() != 'Windows' or 'TRAVIS_TEST' in os.environ:
        st = os.stat(checkpath)
        perm = oct(st.st_mode  & 0o777)
        assert perm == '0o644'