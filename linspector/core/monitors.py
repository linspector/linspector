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
        log('debug', __name__, 'monitor groups: ' + str(monitor_groups))
        monitor_configuration = configparser.ConfigParser()
        for monitor_group in monitor_groups:
            monitors_file_list = glob.glob(self.__configuration.get_configuration_path() +
                                           '/monitors/' + monitor_group + '/*.conf')
            log('debug', __name__, 'monitor files: ' + str(monitors_file_list))
            for monitor_file in monitors_file_list:
                monitor_configuration.read(monitor_file, 'utf-8')

                identifier = monitor_group + '_' + os.path.splitext(os.path.basename(
                    monitor_file))[0]

                # create Monitor() object and copy monitor_configuration for each instance because
                # they else refer to the same object.
                self.__monitors[identifier] = copy.deepcopy(Monitor(configuration, environment, identifier,
                                                      copy.deepcopy(monitor_configuration),
                                                      notifications, services, tasks))

    def get_monitors(self):
        return self.__monitors
