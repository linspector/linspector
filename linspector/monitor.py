"""
This file is part of Linspector (https://linspector.org/)
Copyright (c) 2013-2023 Johannes Findeisen <you@hanez.org>. All Rights Reserved.
See LICENSE.
"""

import configparser
import importlib
import time


class Monitor:
    def __init__(self, configuration, databases, environment, identifier, log,
                 monitor_configuration, notifications, services, tasks, kwargs):
        self._args = kwargs
        self._configuration = configuration
        self._databases = databases
        self._enabled = True
        self._environment = environment
        self._host = monitor_configuration.get('monitor', 'host')

        try:
            self._hostgroups = monitor_configuration.get('monitor', 'hostgroups')
        except configparser.NoOptionError as err:
            self._hostgroups = "None"

        self._identifier = identifier
        self._job_threshold = 0

        try:
            self._interval = int(monitor_configuration.get('monitor', 'interval'))
        except Exception as err:
            log.warning('no interval set in identifier ' + identifier +
                        ', trying to get a monitor configuration setting. error: ' + str(err))

            try:
                self._interval = int(configuration.get_option('linspector', 'default_interval'))
                log.warning('set default_interval as per core configuration with '
                            'identifier: ' + identifier + ' to: ' + str(self._interval))
            except Exception as err:
                log.warning('no default_interval found in core configuration for identifier ' +
                            identifier +
                            ', set to default interval 300 seconds. error: ' + str(err))
                # default interval is 300 seconds (5 minutes) if not set in the monitor
                # configuration args or a default_interval in the core configuration.
                self._interval = 300

        self._log = log
        self._monitor_configuration = monitor_configuration
        self._notification_list = []
        self._notifications = notifications
        self._result = None
        self._scheduler_job = None

        try:
            self._service = monitor_configuration.get('monitor', 'service')
        except Exception as err:
            # if no service is set in the monitor configuration, the service is set to misc.dummy
            # instead. just to make Linspector run but with no real result.
            log.debug('no service set for identifier: ' + identifier + ' setting to '
                                                                       'misc.dummy as '
                                                                       'default to ensure '
                                                                       'Linspector will run. '
                                                                       'error: ' + str(err))

            self._service = 'misc.dummy'

        self._services = services
        self._tasks = tasks

        """
        NONE     job was not executed: -1
        OK       when everything is fine: 0
        WARNING  when a job has errors but the threshold is not overridden: 1
        RECOVER  when a job recovers e.g. the error count decrements: 2
        ERROR    when a jobs error threshold is overridden: 3
        UNKNOWN  when a job throws an exception which is not handled by the job itself: 4
        """
        try:
            notification_list = None
            if configuration.get_option('linspector', 'notifications') or \
                    monitor_configuration.get('monitor', 'notifications'):

                if configuration.get_option('linspector', 'notifications') and \
                        monitor_configuration.get('monitor', 'notifications'):

                    notification_list = \
                        configuration.get_option('linspector', 'notifications') + ',' + \
                        monitor_configuration.get('monitor', 'notifications')
                elif configuration.get_option('linspector', 'notifications'):
                    notification_list = configuration.get_option('linspector', 'notifications')
                elif monitor_configuration.get('monitor', 'notifications'):
                    notification_list = monitor_configuration.get('monitor', 'notifications')

            self._notification_list = notification_list.split(',')

            for notification_option in notification_list.split(','):
                if notification_option not in notifications:
                    notification_package = 'linspector.notifications.' + notification_option.lower()
                    notification_module = importlib.import_module(notification_package)
                    notification = notification_module.create(configuration, environment, log)
                    notifications[notification_option.lower()] = notification
        except configparser.NoOptionError as err:
            self._notifications = notifications

        if self._monitor_configuration.get('monitor', 'service'):
            if monitor_configuration.get('monitor', 'service') not in services:
                service_package = 'linspector.services.' + \
                                  monitor_configuration.get('monitor', 'service').lower()

                service_module = importlib.import_module(service_package)
                self._service = monitor_configuration.get('monitor', 'service').lower()
                service = service_module.create(configuration, environment, log)
                self._services[monitor_configuration.get('monitor', 'service').lower()] = service

    def execute(self):
        self._log.debug('identifier=' + self._identifier + ' object=' + str(self))
        self._log.debug('identifier=' + self._identifier + ' message=handle call to service')

        if self._enabled:
            try:
                self._result = self._services[self._service].execute(self._identifier, self,
                                                                     self._service, **self._args)
                self._log.debug(self._result)
                self._log.debug(self._databases)
                for database in self._databases:
                    self._databases[database].insert(self._result['host'],
                                                     self._identifier,
                                                     self._result,
                                                     self._result['log'],
                                                     self._result['service'],
                                                     self._result['status'],
                                                     int(time.time()))
                    self._log.info(self._result['log'])

                self._log.debug(self._tasks)
                for task in self._tasks:
                    self._tasks[task].execute()
                    self._log.debug("task: " + task)
                    self._log.debug("identifier: " + self._identifier)
                    self._log.debug("service: " + self._service)
                    self._log.debug("status: " + self._result['status'])
                    self._log.debug("log: " + self._result['log'])
                    self._log.debug("json: " + str(self._result))

            except Exception as err:
                self._log.error(err)

        else:
            self._log.info('identifier=' + self._identifier + ' message=is disabled')

    def get_host(self):
        return self._host

    def get_hostgroups(self):
        return self._hostgroups

    def get_identifier(self):
        return self._identifier

    def get_interval(self):
        return self._interval

    def get_monitor_configuration(self):
        return self._monitor_configuration

    def get_monitor_configuration_option(self, section, option):
        if self._monitor_configuration.has_option(section, option):
            return self._monitor_configuration.get(section, option)
        else:
            return None

    def get_service(self):
        return self._service

    def set_enabled(self, enabled=True):
        self._enabled = enabled

    def set_job(self, scheduler_job):
        self._scheduler_job = scheduler_job

    def __str__(self):
        return str(self.__dict__)
