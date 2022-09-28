"""
This file is part of Linspector (https://linspector.org/)
Copyright (c) 2022 Johannes Findeisen <you@hanez.org>. All Rights Reserved.
See LICENSE (MIT license)
"""
import importlib

from logging import getLogger

logger = getLogger('linspector')


class Monitor:

    def __init__(self, configuration, environment, identifier, monitor_configuration, notifications,
                 services, tasks):
        self.__configuration = configuration
        self.__environment = environment
        self.__identifier = identifier
        self.__monitor_configuration = monitor_configuration
        self.__notification_list = []
        self.__service = None
        self.__notifications = notifications
        self.__services = services
        self.__task_list = []  # put tasks for the dedicated job here.
        self.__tasks = tasks

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
                    notification = notification_module.get(configuration, environment)
                    notifications[notification_option.lower()] = notification

        if self.__monitor_configuration.get('monitor', 'service'):
            if monitor_configuration.get('monitor', 'service') not in services:
                service_package = 'linspector.services.' + \
                                  monitor_configuration.get('monitor', 'service').lower()

                service_module = importlib.import_module(service_package)
                self.__service = monitor_configuration.get('monitor', 'service').lower()
                service = service_module.get(configuration, environment)
                services[monitor_configuration.get('monitor', 'service').lower()] = service

            #service.execute(self)

        if configuration.get_option('linspector', 'tasks') or \
                monitor_configuration.get('monitor', 'tasks'):

            if configuration.get_option('linspector', 'tasks') and \
                    monitor_configuration.get('monitor', 'tasks'):

                task_list = configuration.get_option('linspector', 'tasks') + ',' + \
                            monitor_configuration.get('monitor', 'tasks')
            elif configuration.get_option('linspector', 'tasks'):
                task_list = configuration.get_option('linspector', 'tasks')
            elif monitor_configuration.get('monitor', 'tasks'):
                task_list = monitor_configuration.get('monitor', 'tasks')
            else:
                task_list = None

            self.task_list = task_list.split(',')

            for task_option in task_list.split(','):
                if task_option not in tasks:
                    task_package = 'linspector.tasks.' + task_option.lower()
                    task_module = importlib.import_module(task_package)
                    task = task_module.get(configuration, environment)
                    tasks[task_option.lower()] = task

    def get_identifier(self):
        return self.__identifier

    # currently only used for testing but maybe i will add get functions for all known variables.
    # but not all variables can be known because all monitors are different. only the service
    # implementation can know all variables which are being used inside the service.
    def get_service(self):
        return self.__monitor_configuration.get('monitor', 'service')
