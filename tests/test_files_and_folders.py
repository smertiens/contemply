#
# Contemply - A code generator that creates boilerplate files from templates
#
# Copyright (C) 2019  Sean Mertiens
# For more information on licensing see LICENSE file
#
import pytest
import os

def test_access_upstream_folders_from_cwd(tmpdir, monkeypatch):
    # will be used later
    root = str(tmpdir)
    new_cwd = os.path.join(root, 'foo', 'bar')
    os.makedirs(new_cwd)
    os.getcwd()

    monkeypatch.setattr(os, 'getcwd', lambda: new_cwd)

    assert os.getcwd() == new_cwd

