#
# Contemply - A code generator that creates boilerplate files from templates
#
# Copyright (C) 2019  Sean Mertiens
# For more information on licensing see LICENSE file
#

from contemply.preferences import PreferencesProvider
import os


def test_create_and_save_file(tmpdir):
    # overwrite settings file
    os.environ['CONTEMPLY_SETTINGS_FILE'] = os.path.join(str(tmpdir), 'settings.json')

    assert not os.path.exists(os.environ['CONTEMPLY_SETTINGS_FILE'])

    pref = PreferencesProvider()
    pref.save()

    assert os.path.exists(os.environ['CONTEMPLY_SETTINGS_FILE'])


def test_save_and_load(tmpdir):
    # overwrite settings file
    os.environ['CONTEMPLY_SETTINGS_FILE'] = os.path.join(str(tmpdir), 'settings.json')

    pref = PreferencesProvider()
    pref.set('hello', 'world')
    pref.save()
    pref = None

    pref2 = PreferencesProvider()
    assert pref2.get('hello') == 'world'


def test_get_default(tmpdir):
    # overwrite settings file
    os.environ['CONTEMPLY_SETTINGS_FILE'] = os.path.join(str(tmpdir), 'settings.json')

    pref = PreferencesProvider()
    assert pref.get('not_existing', 'default') == 'default'
