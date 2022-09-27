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
import copy
import glob
import os

from logging import getLogger

from linspector.core.monitor import Monitor


logger = getLogger('linspector')


# monitors may could / should be added (and maybe changed) at runtime to add new monitors without
# restarting the daemon. maybe add a reset function to each monitor to reset the monitor at runtime
# when changed dynamically.
class Monitors:

    def __init__(self, configuration, environment, notifications, services, tasks):
        self.__configuration = configuration
        self.__environment = environment
        self.__monitors = {}

        monitor_groups = os.listdir(self.__configuration.get_configuration_path() + '/monitors/')
        #print(__file__ + ' (47): ' + str(monitor_groups))
        monitor_configuration = configparser.ConfigParser()
        for monitor_group in monitor_groups:
            monitors_file_list = glob.glob(self.__configuration.get_configuration_path() +
                                           '/monitors/' + monitor_group + '/*.conf')

            for monitor_file in monitors_file_list:
                monitor_configuration.read(monitor_file, 'utf-8')

                identifier = monitor_group + '_' + os.path.splitext(os.path.basename(
                    monitor_file))[0]

                # create Monitor() object and copy monitor_configuration for each instance because
                # they else refer to the same object.
                self.__monitors[identifier] = Monitor(configuration, environment, identifier,
                                                      copy.deepcopy(monitor_configuration),
                                                      notifications, services, tasks)

    def get_monitors(self):
        return self.__monitors
