#
# Contemply - A code generator that creates boilerplate files from templates
#
# Copyright (C) 2019  Sean Mertiens
# For more information on licensing see LICENSE file
#

import os
import pytest
import sys

import contemply.bundles.pythonbundle.cpy_extension as pythonbundle
from contemply import cli
from contemply.parser import TemplateContext


def test_create_venv(tmpdir, monkeypatch):
    tmpdir = str(tmpdir)
    os.chdir(tmpdir)

    assert os.path.abspath('.') == tmpdir

    assert not os.path.exists(tmpdir + '/.venv')
    pythonbundle.make_venv([['colorama']], TemplateContext())
    assert os.path.exists(tmpdir + '/.venv')

    colorama_path = tmpdir + '/.venv/lib/python{}.{}/site-packages/colorama'.format(sys.version_info[0],
                                                                                    sys.version_info[1])
    assert os.path.exists(colorama_path)


def test_create_venv_fail_on_package_install(tmpdir, monkeypatch):
    def check_prompt(q, d):
        if not q == 'Could not install package "contemply_package_does_not_exist" to venv. Do you want to continue parsing this template?':
            pytest.fail('no prompt issued on failed package install')

        return True

    tmpdir = str(tmpdir)
    os.chdir(tmpdir)
    monkeypatch.setattr(cli, 'prompt', check_prompt)

    pythonbundle.make_venv([['contemply_package_does_not_exist']], TemplateContext())
