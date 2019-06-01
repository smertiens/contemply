#
# Contemply - A code generator that creates boilerplate files from templates
#
# Copyright (C) 2019  Sean Mertiens
# For more information on licensing see LICENSE file
#

from click.testing import CliRunner
from contemply.contemply_cli import version, header, cli, run


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

def test_run_command():
    runner = CliRunner()

    # no args
    result = runner.invoke(run)
    assert result.exit_code != 0


    
