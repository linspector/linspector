"""
This file is part of Linspector (https://linspector.org/)
Copyright (c) 2013-2023 Johannes Findeisen <you@hanez.org>. All Rights Reserved.
See LICENSE.
"""

import configparser
import glob
import os


class Configuration:
    def __init__(self, configuration_path):
        self._configuration = configparser.ConfigParser()
        self._configuration_path = configuration_path

        print('Reading configuration file: ' + configuration_path + '/linspector.conf')
        if os.path.isfile(configuration_path + '/linspector.conf'):
            try:
                self._configuration.read(configuration_path + '/linspector.conf', 'utf-8')
            except Exception as err:
                raise Exception('something went wrong reading the configuration file '
                                'linspector.conf in the configuration root path! ({0})'.format(err))
        else:
            raise FileNotFoundError("configuration file linspector.ini not found in configuration "
                                    "root path!")

        # add keys and values defined in sub dirs and configuration ini files.
        for target_section in ['databases', 'notifications', 'plugins', 'services', 'tasks']:
            # check if section exists before adding content. if not exists add the section.
            if not self._configuration.has_section(target_section):
                self._configuration.add_section(target_section)

            section_list = glob.glob(configuration_path + '/' + target_section + '/*.conf')
            for section_file in section_list:
                # print('reading section file: ' + section_file)
                configuration = configparser.ConfigParser()
                configuration.read(section_file, 'utf-8')
                for source_section in configuration.sections():
                    source_section_options = configuration.options(source_section)
                    for source_section_option in source_section_options:
                        self._configuration.set(target_section, source_section + '_' +
                                                source_section_option,
                                                configuration.get(source_section,
                                                                  source_section_option))

        # print('configuration dump: ' + self.dump_to_ini())

    def dump_to_ini(self):
        dump = ''
        i = 0
        for section in self._configuration.sections():
            if i < 1:
                dump = dump + '[' + section + ']\n'
            else:
                dump = dump + '\n[' + section + ']\n'
            options = self._configuration.options(section)
            for option in options:
                dump = dump + option + " = " + self._configuration.get(section, option) + '\n'
            i = 1
        return dump

    def get_configuration_path(self):
        return self._configuration_path

    def get_option(self, section, option):
        if self._configuration.has_option(section, option):
            return self._configuration.get(section, option)
        else:
            return None

    # this function should be used with care because it edits the main configuration. maybe it can
    # be used for dynamic runtime configuration later but i need to think about it.
    def set_option(self, section, option, value):
        if not self._configuration.has_option(section, option):
            self._configuration.set(section, option, value)
