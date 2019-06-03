#
# Contemply - A code generator that creates boilerplate files from templates
#
# Copyright (C) 2019  Sean Mertiens
# For more information on licensing see LICENSE file
#

import os
import pytest

from click.testing import CliRunner
from contemply.contemply_cli import version, header, cli, run
from contemply.preferences import PreferencesProvider
from contemply.storage import TemplateStorageManager


@pytest.fixture()
def pref_instance(tmpdir):
    os.environ['CONTEMPLY_SETTINGS_FILE'] = os.path.join(str(tmpdir), 'settings.json')
    pref = PreferencesProvider()
    return pref


def test_no_command():
    runner = CliRunner()
    result = runner.invoke(cli)

    assert result.exit_code == 0
    assert 'Usage: ' in result.output


def test_version_command():
    runner = CliRunner()
    result = runner.invoke(version)

    assert result.exit_code == 0
    assert 'Contemply version ' in result.output


def test_storage_add(pref_instance, tmpdir):
    tmpdir = str(tmpdir)

    runner = CliRunner()
    result = runner.invoke(cli, ['storage:add', 'demo', tmpdir])
    assert result.exit_code == 0
    assert 'has been added' in result.output

    pref_instance.load()
    storage = TemplateStorageManager(pref_instance)
    assert 'demo' in storage.list()


def test_storage_list(pref_instance, tmpdir):
    tmpdir = str(tmpdir)

    storage = TemplateStorageManager(pref_instance)
    assert storage.list() == {}
    storage.add_location('some_name', tmpdir)

    runner = CliRunner()
    result = runner.invoke(cli, ['storage:list'])
    assert result.exit_code == 0
    assert tmpdir in result.output


def test_storage_remove(pref_instance, tmpdir):
    tmpdir = str(tmpdir)

    storage = TemplateStorageManager(pref_instance)
    assert storage.list() == {}
    storage.add_location('some_name', tmpdir)
    assert 'some_name' in storage.list()

    runner = CliRunner()
    result = runner.invoke(cli, ['storage:remove', 'some_name'])
    assert result.exit_code == 0
    assert 'removed' in result.output

    pref_instance.load()
    storage = TemplateStorageManager(pref_instance)
    assert storage.list() == {}


def test_storage_show(pref_instance, tmpdir):
    tmpdir = str(tmpdir)

    storage = TemplateStorageManager(pref_instance)
    assert storage.list() == {}
    storage.add_location('some_name', tmpdir)
    assert 'some_name' in storage.list()

    runner = CliRunner()
    result = runner.invoke(cli, ['storage:show', 'some_name'])
    assert result.exit_code == 0
    assert 'Found 1 template.' in result.output
    assert 'settings.json' in result.output


def test_run_command(tmpdir):
    tmpdir = str(tmpdir)
    testfile = tmpdir + '/' + 'demo.pytpl'

    # no args
    runner = CliRunner()
    result = runner.invoke(run)
    assert result.exit_code != 0

    # create a demo file
    with open(testfile, 'w') as f:
        f.write('\n'.join([
            '#: echo("Hello World!")',
            '#: setOutput("./demo.txt")',
            'Contentline'
        ]))

    # run file
    runner = CliRunner()
    result = runner.invoke(cli, ['run', testfile])

    assert result.exit_code == 0
    assert os.path.exists('./demo.txt')
    assert 'Hello World!' in result.output
    assert 'has been created' in result.output
    assert header(True) in result.output

    # cleanup
    os.unlink('./demo.txt')
    assert not os.path.exists('./demo.txt')

    # run file and output to console
    runner = CliRunner()
    result = runner.invoke(cli, ['run', '-p', testfile])

    assert result.exit_code == 0
    assert not os.path.exists('./demo.txt')
    assert 'Hello World!' in result.output
    assert 'Contentline' in result.output
    assert header(True) in result.output

    # run file and output to console without header
    runner = CliRunner()
    result = runner.invoke(cli, ['run', '--print', '--no-header', testfile])

    assert result.exit_code == 0
    assert not os.path.exists('./demo.txt')
    assert 'Hello World!' in result.output
    assert 'Contentline' in result.output
    assert not header(True) in result.output
