#
# Contemply - A code generator that creates boilerplate files from templates
#
# Copyright (C) 2019  Sean Mertiens
# For more information on licensing see LICENSE file
#
import os
import re

from contemply.exceptions import *

def get_secure_path(base, path):
    final_path = os.path.realpath(os.path.join(base, path))
    real_base = os.path.realpath(base)

    if not final_path.startswith(real_base):
        raise SecurityException('Attempt to access path above the given base directory blocked.')

    return final_path

class TemplateStorageManager:

    def __init__(self, pref_provider):
        """

        :param PreferencesProvider pref_provider: A PreferencesProvider instance
        """
        self._preferences = pref_provider
        self._locations = self._preferences.get('storage_locations', {})

    def is_valid_storage_name(self, name):
        """
        Checks whether the given storage name is valid

        :param str name: The name of the storage
        :return: True or False
        :rtype: bool
        """

        return re.match(r'^[a-zA-Z0-9_\.]+$', name) is not None

    def add_location(self, name, path):
        """

        :param str name: The name of the location
        :param str path: The absolute path to the location
        :raises: StorageException
        """

        if not self.is_valid_storage_name(name):
            raise InvalidStorageNameException(
                'Invalid name for the new storage. Use only alphanumeric character, . and _')

        if name in self._locations:
            raise StorageNameExistsException('The given storage already exists.')

        self._locations[name] = os.path.abspath(path)
        self._persist()

    def remove_location(self, name):
        """

        :param str name: The name of the location to remove
        :raises: StorageException
        """

        if not name in self._locations:
            raise StorageNameNotFoundException('The given storage was not found.')

        del self._locations[name]
        self._persist()

    def resolve(self, template_name):
        """

        :param str template_name: The template string to resolve
        :return: The absolute path to the template folder
        :rtype: str
        """

        name, template = template_name.split('::')

        if not name in self._locations:
            raise StorageNameNotFoundException('The given storage was not found.')

        path = self._locations[name]
        return get_secure_path(path, template)

    def list(self):
        """
        Returns a list  with the current storage locations
        :return: List of storage locations (as dictionary)
        :rtype: dict
        """

        return self._locations

    def _persist(self):
        """
        Persist locations to settings
        """

        self._preferences.set('storage_locations', self._locations)
        self._preferences.save()
