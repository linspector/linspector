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
# when changed dynamically. better: add a hash of the config file of each monitor to each monitor
# object and if it has changed reload the monitor. e.g. delete it from the scheduler and reschedule.
# if a new monitor is added at runtime it needs to be checked manually by running a "reload" command
# to lish which walks thrue all scheduled jobs and when an unknown monitor is found, schedule it.
class Monitors:
    def __init__(self, configuration, environment, log, notifications, services, tasks):
        self._configuration = configuration
        self._environment = environment
        self._log = log
        self._notifications = notifications
        self._monitors = {}
        self._services = services
        self._tasks = tasks

        monitor_groups = os.listdir(self._configuration.get_configuration_path() + '/monitors/')
        log.debug('monitor groups: ' + str(monitor_groups))
        for monitor_group in monitor_groups:
            monitors_file_list = glob.glob(self._configuration.get_configuration_path() +
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
                self._monitors[identifier] = Monitor(self._configuration,
                                                     self._environment,
                                                     identifier,
                                                     self._log,
                                                     monitor_configuration,
                                                     self._notifications,
                                                     self._services,
                                                     self._tasks,
                                                     kwargs)

                del kwargs

    def get_monitors(self):
        return self._monitors
