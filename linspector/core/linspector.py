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
import importlib

from logging import getLogger

logger = getLogger('linspector')


class Linspector:

    def __init__(self, configuration, environment, monitors, plugins):
        self.__configuration = configuration
        self.__environment = environment
        self.__monitors = monitors
        self.__plugin_list = None
        self.__plugins = plugins

        # load plugins
        if configuration.get_option('linspector', 'plugins'):
            plugin_list = configuration.get_option('linspector', 'plugins')
            self.__plugin_list = plugin_list.split(',')
            for plugin_option in plugin_list.split(','):
                if plugin_option not in plugins:
                    plugin_package = 'linspector.plugins.' + plugin_option.lower()
                    plugin_module = importlib.import_module(plugin_package)
                    plugin = plugin_module.get(configuration, environment, self)
                    plugins[plugin_option.lower()] = plugin

    # this function is just for testing purposes and can be removed some day
    def print_debug(self):
        # example on how to access the monitor objects in monitors
        monitors = self.__monitors.get_monitors()
        print(__file__ + ' (59): ' + str(monitors))
        for monitor in monitors:
            print(__file__ + ' (61): ' + monitors.get(monitor).get_identifier())
            print(__file__ + ' (62): ' + monitors.get(monitor).get_service())
