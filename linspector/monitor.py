"""
This file is part of Linspector (https://linspector.org/)
Copyright (c) 2022 Johannes Findeisen <you@hanez.org>. All Rights Reserved.
See LICENSE (MIT license).
"""
import configparser
import importlib


class Monitor:
    def __init__(self, configuration, environment, identifier, log, monitor_configuration,
                 notifications, services, tasks, kwargs):
        self.__args = kwargs
        self.__configuration = configuration
        self.__enabled = True
        self.__environment = environment
        self.__host = monitor_configuration.get('monitor', 'host')

        try:
            self.__hostgroups = monitor_configuration.get('monitor', 'hostgroups')
        except configparser.NoOptionError as err:
            self.__hostgroups = "None"

        self.__identifier = identifier
        self.__job_threshold = 0

        try:
            self.__interval = int(monitor_configuration.get('monitor', 'interval'))
        except Exception as err:
            log.warning('no interval set in identifier ' + identifier +
                        ', trying to get a monitor configuration setting. error: ' + str(err))

            try:
                self.__interval = int(configuration.get_option('linspector', 'default_interval'))
                log.warning('set default_interval as per core configuration with '
                            'identifier: ' + identifier + ' to: ' + str(self.__interval))
            except Exception as err:
                log.warning('no default_interval found in core configuration for identifier ' +
                            identifier +
                            ', set to default interval 300 seconds. error: ' + str(err))
                # default interval is 300 seconds (5 minutes) if not set in the monitor
                # configuration args or a default_interval in the core configuration.
                self.__interval = 300

        self.__log = log
        self.__monitor_configuration = monitor_configuration
        self.__notification_list = []
        self.__notifications = notifications
        self.__scheduler_job = None

        try:
            self.__service = monitor_configuration.get('monitor', 'service')
        except Exception as err:
            # if no service is set in the monitor configuration, the service is set to misc.dummy
            # instead. just to make Linspector run but with no real result.
            log.debug('no service set for identifier: ' + identifier + ' setting to '
                                                                       'misc.dummy as '
                                                                       'default to ensure '
                                                                       'Linspector will run. '
                                                                       'error: ' + str(err))

            self.__service = 'misc.dummy'

        self.__services = services
        self.__task_list = []  # put tasks for the dedicated job here.
        self.__tasks = tasks

        """
        NONE     job was not executed
        OK       when everything is fine
        WARNING  when a job has errors but the threshold is not overridden
        RECOVER  when a job recovers e.g. the threshold decrements (not implemented)
        ERROR    when a jobs error threshold is overridden
        UNKNOWN  when a job throws an exception which is not handled by the job itself (not 
        implemented)
        self.status = "NONE"
        self.last_execution = None
        """

        try:
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
                else:
                    notification_list = None

                self.__notification_list = notification_list.split(',')

            for notification_option in notification_list.split(','):
                if notification_option not in notifications:
                    notification_package = 'linspector.notifications.' + notification_option.lower()
                    notification_module = importlib.import_module(notification_package)
                    notification = notification_module.create(configuration, environment, log)
                    notifications[notification_option.lower()] = notification
        except configparser.NoOptionError as err:
            self.__notifications = notifications

        if self.__monitor_configuration.get('monitor', 'service'):
            if monitor_configuration.get('monitor', 'service') not in services:
                service_package = 'linspector.services.' + \
                                  monitor_configuration.get('monitor', 'service').lower()

                service_module = importlib.import_module(service_package)
                self.__service = monitor_configuration.get('monitor', 'service').lower()
                service = service_module.create(configuration, environment, log)
                self.__services[monitor_configuration.get('monitor', 'service').lower()] = service
        try:
            if configuration.get_option('linspector', 'tasks') or \
                    monitor_configuration.get('args', 'tasks'):

                if configuration.get_option('linspector', 'tasks') and \
                        monitor_configuration.get('args', 'tasks'):

                    task_list = configuration.get_option('linspector', 'tasks') + ',' + \
                                monitor_configuration.get('args', 'tasks')
                elif configuration.get_option('linspector', 'tasks'):
                    task_list = configuration.get_option('linspector', 'tasks')
                elif monitor_configuration.get('args', 'tasks'):
                    task_list = monitor_configuration.get('args', 'tasks')
                else:
                    task_list = None

                self.__task_list = task_list.split(',')

                for task_option in task_list.split(','):
                    if task_option not in tasks:
                        task_package = 'linspector.tasks.' + task_option.lower()
                        task_module = importlib.import_module(task_package)
                        task = task_module.create(configuration, environment, log)
                        tasks[task_option.lower()] = task
        except configparser.NoOptionError:
            self.__tasks = tasks

    def execute(self):
        self.__log.debug('identifier=' + self.__identifier + ' object=' + str(self))
        self.__log.debug('identifier=' + self.__identifier + ' message=handle call to service')

        if self.__enabled:
            try:
                self.__services[self.__service].execute(self.__identifier, self, self.__service,
                                                        **self.__args)
            except Exception as err:
                self.__log.error(err)
        else:
            self.__log.info('identifier=' + self.__identifier + ' message=is disabled')

    def get_host(self):
        return self.__host

    def get_hostgroups(self):
        return self.__hostgroups

    def get_identifier(self):
        return self.__identifier

    def get_interval(self):
        return self.__interval

    def get_monitor_configuration(self):
        return self.__monitor_configuration

    def get_monitor_configuration_option(self, section, option):
        if self.__monitor_configuration.has_option(section, option):
            return self.__monitor_configuration.get(section, option)
        else:
            return None

    def get_service(self):
        return self.__service

    def set_enabled(self, enabled=True):
        self.__enabled = enabled

    def set_job(self, scheduler_job):
        self.__scheduler_job = scheduler_job

    def __str__(self):
        return str(self.__dict__)
