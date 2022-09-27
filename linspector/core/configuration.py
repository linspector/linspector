"""
This file is part of Linspector (https://linspector.org/)
Copyright (c) 2022 Johannes Findeisen <you@hanez.org>. All Rights Reserved.

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is furnished
to do so, subject to the following conditions:

The above copyright notice and this permission notice (including the next
paragraph) shall be included in all copies or substantial portions of the
Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS
FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS
OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY,
WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF
OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
"""

import configparser
import glob
import os

from logging import getLogger

logger = getLogger('linspector')


# TODO: check for all required configuration options and set defaults if needed. do this only for
#  options in the "linspector" section of linspector.ini.
class Configuration:

    def __init__(self, configuration_path, environment):
        self.__configuration = configparser.ConfigParser()
        self.__configuration_path = configuration_path
        self.__environment = environment

        if os.path.isfile(configuration_path + '/linspector.ini'):
            try:
                self.__configuration.read(configuration_path + '/linspector.ini', 'utf-8')
            except Exception as err:
                raise Exception('something went wrong reading the configuration file '
                                'linspector.ini in the configuration root path! ({0})'.format(err))
        else:
            raise FileNotFoundError("configuration file linspector.ini not found in configuration "
                                    "root path!")

        # add keys and values defined in sub dirs and configuration ini files.
        for target_section in ['notifications', 'plugins', 'services', 'tasks']:
            # check if section exists before adding content. if not exists add the section.
            if not self.__configuration.has_section(target_section):
                self.__configuration.add_section(target_section)

            section_list = glob.glob(configuration_path + '/' + target_section + '/*.ini')
            for section_file in section_list:
                #print(__file__ + ' (60): ' + section_file)
                configuration = configparser.ConfigParser()
                configuration.read(section_file, 'utf-8')
                for source_section in configuration.sections():
                    source_section_options = configuration.options(source_section)
                    for source_section_option in source_section_options:
                        self.__configuration.set(target_section, source_section + '_' +
                                                 source_section_option,
                                                 configuration.get(source_section,
                                                                   source_section_option))

    def dump_to_ini(self):
        i = 0
        for section in self.__configuration.sections():
            if i < 1:
                print('[' + section + ']')
            else:
                print('\n[' + section + ']')
            options = self.__configuration.options(section)
            for option in options:
                print(option + " = " + self.__configuration.get(section, option))
            i = 1

    def get_configuration_path(self):
        return self.__configuration_path

    def get_option(self, section, option):
        if self.__configuration.has_option(section, option):
            return self.__configuration.get(section, option)
        else:
            return None

    # this function should be used with care because it edits the main configuration. maybe it can
    # be used for dynamic runtime configuration later but i need to think about it.
    def set_option(self, section, option, value):
        if not self.__configuration.has_option(section, option):
            self.__configuration.set(section, option, value)
