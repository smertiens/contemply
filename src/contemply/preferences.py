#
# Contemply - A code generator that creates boilerplate files from templates
#
# Copyright (C) 2019  Sean Mertiens
# For more information on licensing see LICENSE file
#
import json
import logging
import os
import platform
from io import StringIO


class PreferencesProvider:

    def __init__(self):
        self.settings = {}
        self.load()

    def get(self, name, default=None):
        if name in self.settings:
            return self.settings[name]
        elif default is not None:
            return default

    def set(self, name, val):
        self.settings[name] = val

    def load(self):
        if not os.path.exists(self._get_settings_file('settings.json')):
            return

        with open(self._get_settings_file('settings.json'), 'r') as f:
            contents = f.read()

        data = StringIO(contents)
        try:
            obj = json.load(data)
            self.settings = obj
        except json.JSONDecodeError:
            self.get_logger().error('Unable to read settings file')
            return

    def save(self):
        out = StringIO()
        json.dump(self.settings, out)
        json_data = out.getvalue()

        with open(self._get_settings_file('settings.json'), 'w') as f:
            f.write(json_data)

        self.get_logger().debug('Settings saved')

    def _get_settings_file(self, fname=''):

        if 'CONTEMPLY_SETTINGS_FILE' in os.environ:
            return os.environ['CONTEMPLY_SETTINGS_FILE']

        user_dir = os.path.expanduser('~')

        if platform.system() == 'Windows':
            user_dir = os.path.join(user_dir, "contemply")
        else:
            user_dir = os.path.join(user_dir, ".contemply")

        if not os.path.exists(user_dir):
            self.get_logger().info('User dir does not exist. Creating {0}'.format(user_dir))
            os.makedirs(user_dir)

        return os.path.join(user_dir, fname)

    def get_logger(self):
        return logging.getLogger(self.__module__)
