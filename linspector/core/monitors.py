"""
This file is part of Linspector (https://linspector.org/)
Copyright (c) 2022 Johannes Findeisen <you@hanez.org>. All Rights Reserved.
See LICENSE (MIT license)
"""
import configparser
import copy
import glob
import os

from linspector.core.monitor import Monitor
from linspector.core.helpers import log


# monitors may could / should be added (and maybe changed) at runtime to add new monitors without
# restarting the daemon. maybe add a reset function to each monitor to reset the monitor at runtime
# when changed dynamically.
class Monitors:

    def __init__(self, configuration, environment, notifications, services, tasks):
        self.__configuration = configuration
        self.__environment = environment
        self.__monitors = {}

        monitor_groups = os.listdir(self.__configuration.get_configuration_path() + '/monitors/')
        log('debug', 'monitor groups: ' + str(monitor_groups))
        for monitor_group in monitor_groups:
            monitors_file_list = glob.glob(self.__configuration.get_configuration_path() +
                                           '/monitors/' + monitor_group + '/*.conf')

            log('debug', 'monitor files: ' + str(monitors_file_list))
            for monitor_file in monitors_file_list:
                identifier = monitor_group + '_' + os.path.splitext(os.path.basename(
                    monitor_file))[0]

                monitor_configuration = configparser.ConfigParser()
                monitor_configuration.read(monitor_file, 'utf-8')

                kwargs = {}
                for option in monitor_configuration.options('args'):
                    value = monitor_configuration.get('args', option)
                    #log('debug', 'added option to kwargs: ' + option + ' = ' + value)
                    kwargs[option] = value

                if kwargs:
                    log('debug', identifier + ' args ' + str(kwargs))

                identifier = monitor_group + '_' + os.path.splitext(os.path.basename(
                    monitor_file))[0]

                # create Monitor() object and copy monitor_configuration for each instance because
                # they else refer to the same object.
                self.__monitors[identifier] = Monitor(configuration, environment, identifier,
                                                      monitor_configuration, notifications,
                                                      services, tasks, copy.deepcopy(kwargs))

                del kwargs

    def get_monitors(self):
        return self.__monitors
