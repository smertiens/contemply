#
# Contemply - A code generator that creates boilerplate files from templates
#
# Copyright (C) 2019  Sean Mertiens
# For more information on licensing see LICENSE file
#

from contemply.storage import *
from contemply.preferences import PreferencesProvider
import pytest
import os


@pytest.fixture()
def pref_instance(tmpdir):
    os.environ['CONTEMPLY_SETTINGS_FILE'] = os.path.join(str(tmpdir), 'settings.json')
    pref = PreferencesProvider()
    return pref


def test_add_path(pref_instance, tmpdir):
    storage = TemplateStorageManager(pref_instance)
    assert storage.list() == {}

    storage.add_location('some_name', str(tmpdir))
    assert storage.resolve('some_name::hello.pytpl') == os.path.join(str(tmpdir), 'hello.pytpl')
    assert 'some_name' in storage.list()


def test_remove_path(pref_instance, tmpdir):
    storage = TemplateStorageManager(pref_instance)
    assert storage.list() == {}
    storage.add_location('some_name', str(tmpdir))
    assert 'some_name' in storage.list()

    storage.remove_location('some_name')
    assert not 'some_name' in storage.list()

    with pytest.raises(StorageNameNotFoundException):
        storage.remove_location('does_not_exist')

def test_list(pref_instance, tmpdir):
    tmpdir = str(tmpdir)
    storage = TemplateStorageManager(pref_instance)

    # create demo files
    files = ['demo1.pytpl', 'demo2.pytpl']
    for file in files:
        with open(tmpdir + '/' +file, 'w') as f:
            f.write('#')

        assert os.path.exists(tmpdir + '/' +file)

    assert storage.list() == {}
    storage.add_location('my_templates', tmpdir)
    assert 'my_templates' in storage.list()

    items = storage.show('my_templates')
    for file in files:
        assert file in items


def test_check_name(pref_instance):
    storage = TemplateStorageManager(pref_instance)
    data = {
        'hello_world': True,
        'hello': True,
        'hello12200': True,
        '2233_asdaodkopo': True,
        'adaosijd adad': False,
        'adoapksd:asdasd': False,
        'adasd.asdsd23': True
    }

    for name, expected in data.items():
        assert storage.is_valid_storage_name(name) == expected, 'Checking ' + name


def test_access_upstream_folders(pref_instance, tmpdir):
    storage = TemplateStorageManager(pref_instance)
    assert storage.list() == {}

    root = str(tmpdir)
    storage_dir = os.path.join(root, 'foo', 'bar')
    os.makedirs(storage_dir)

    storage.add_location('my_storage', storage_dir)
    assert 'my_storage' in storage.list()

    assert storage.resolve('my_storage::hello.pytpl') == os.path.join(storage_dir, 'hello.pytpl')
    assert storage.resolve('my_storage::./hello.pytpl') == os.path.join(storage_dir, 'hello.pytpl')

    with pytest.raises(SecurityException):
        assert storage.resolve('my_storage::../hello.pytpl') == os.path.join(root, 'foo', 'hello.pytpl')

    with pytest.raises(SecurityException):
        assert storage.resolve('my_storage::../../.././../hello.pytpl') == 'Something'