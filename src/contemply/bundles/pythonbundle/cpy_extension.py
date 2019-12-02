#
# Contemply - A code generator that creates boilerplate files from templates
#
# Copyright (C) 2019  Sean Mertiens
# For more information on licensing see LICENSE file
#

import os
import subprocess
import venv

from contemply import cli, util


def make_venv(args, ctx):
    util.check_function_args(['make_venv', '*list'], args)
    install_packages = args[0] if len(args) == 1 else []

    target_dir = os.path.abspath('./.venv')
    venv.create(env_dir=target_dir, with_pip=True)

    pip_path = os.path.join(target_dir, 'bin', 'pip3')

    if len(install_packages) > 0:
        # we have to ensure pip is installed
        assert os.path.exists(pip_path)

    for package in install_packages:
        r = subprocess.run([pip_path, 'install', package])

        if r.returncode != 0:
            if not cli.prompt(
                    'Could not install package "%s" to venv. Do you want to continue parsing this template?' % package,
                    'No'):
                ctx.stop()
