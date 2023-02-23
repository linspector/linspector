"""
This file is part of Linspector (https://linspector.org/)
Copyright (c) 2022 Johannes Findeisen <you@hanez.org>. All Rights Reserved.
See LICENSE (MIT license).
"""
import configparser
import glob
import os

from linspector.monitor import Monitor


# monitors may must / should be added (and maybe changed) at runtime to add new monitors without
# restarting the daemon. maybe add a reset function to each monitor to reset the monitor at runtime
# when changed dynamically.
class Monitors:
    def __init__(self, configuration, environment, log, notifications, services, tasks):
        self.__configuration = configuration
        self.__environment = environment
        self.__log = log
        self.__notifications = notifications
        self.__monitors = {}
        self.__services = services
        self.__tasks = tasks

        monitor_groups = os.listdir(self.__configuration.get_configuration_path() + '/monitors/')
        log.debug('monitor groups: ' + str(monitor_groups))
        for monitor_group in monitor_groups:
            monitors_file_list = glob.glob(self.__configuration.get_configuration_path() +
                                           '/monitors/' + monitor_group + '/*.conf')

            log.debug('monitor files: ' + str(monitors_file_list))
            for monitor_file in monitors_file_list:
                identifier = monitor_group + '.' + os.path.splitext(os.path.basename(
                    monitor_file))[0]

                monitor_configuration = configparser.ConfigParser()
                monitor_configuration.read(monitor_file, 'utf-8')

                kwargs = {}
                for option in monitor_configuration.options('args'):
                    value = monitor_configuration.get('args', option)
                    log.debug('added option in ' + identifier + ' to kwargs: ' + option + ' = ' +
                              value)

                    kwargs[option] = value

                if kwargs:
                    log.debug(identifier + ' args ' + str(kwargs))

                identifier = monitor_group + '.' + os.path.splitext(os.path.basename(
                    monitor_file))[0]

                # create Monitor() object and copy monitor_configuration for each instance because
                # they else refer to the same object? copy.deepcopy(monitor_configuration)???
                self.__monitors[identifier] = Monitor(self.__configuration,
                                                      self.__environment,
                                                      identifier,
                                                      self.__log,
                                                      monitor_configuration,
                                                      self.__notifications,
                                                      self.__services,
                                                      self.__tasks,
                                                      kwargs)

                del kwargs

    def get_monitors(self):
        return self.__monitors
