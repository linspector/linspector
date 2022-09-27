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


class Monitor:

    def __init__(self, configuration, environment, identifier, monitor_configuration, notifications,
                 services, tasks):
        self.__configuration = configuration
        self.__environment = environment
        self.__identifier = identifier
        self.__monitor_configuration = monitor_configuration
        self.__notification_list = []
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

            self.__notification_list = notification_list

            for notification_option in notification_list.split(','):
                #print(__file__ + ' (64): ' + str(notification_option))
                if notification_option not in notifications:
                    notification_package = 'linspector.notifications.' + notification_option.lower()
                    notification_module = importlib.import_module(notification_package)
                    notification = getattr(notification_module, notification_option +
                                           'Notification')

                    notification.__init__(self, configuration, environment)
                    notifications[notification_option] = notification
                    #print(__file__ + ' (73): ' + str(notifications))

        #print(__file__ + ' (75): ' + str(monitor_configuration))
        if self.__monitor_configuration.get('monitor', 'service'):
            if monitor_configuration.get('monitor', 'service') not in services:
                service_package = 'linspector.services.' + \
                                  monitor_configuration.get('monitor', 'service').lower()

                service_module = importlib.import_module(service_package)
                service = getattr(service_module,
                                  monitor_configuration.get('monitor', 'service') + 'Service')

                service.__init__(self, configuration, environment)
                services[monitor_configuration.get('monitor', 'service')] = service
                #print(__file__ + ' (87): ' + str(services))

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

            self.task_list = task_list

            for task_option in task_list.split(','):
                if task_option not in tasks:
                    #print(__file__ + ' (110): ' + str(task_option))
                    task_package = 'linspector.tasks.' + task_option.lower()
                    task_module = importlib.import_module(task_package)
                    task = getattr(task_module, task_option + 'Task')
                    task.__init__(self, configuration, environment)
                    tasks[task_option] = task

            #print(__file__ + ' (117): ' + str(tasks))

    def get_identifier(self):
        return self.__identifier

    # currently only used for testing but maybe i will add get functions for all known variables.
    # but not all variables can be known because all monitors are different. only the service
    # implementation can know all variables which are being used inside the service.
    def get_service(self):
        return self.__monitor_configuration.get('monitor', 'service')
