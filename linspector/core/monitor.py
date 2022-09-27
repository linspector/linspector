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
                 services):
        self.__configuration = configuration
        self.__environment = environment
        self.__identifier = identifier
        self.__monitor_configuration = monitor_configuration
        self.__notifications = notifications
        self.__services = services

        #print(__file__ + ' (42): ' + str(monitor_configuration))
        if self.__monitor_configuration.get('monitor', 'service'):

            # TODO: the exception handling later!!!
            #try:
            service_package = 'linspector.services.' + \
                              self.__monitor_configuration.get('monitor', 'service').lower()
            service_module = importlib.import_module(service_package)

            service = getattr(service_module, self.__monitor_configuration.get('monitor', 'service') +
                              'Service')
            service.__init__(self, configuration, environment)

            if self.__monitor_configuration.get('monitor', 'service') not in services:
                services[self.__monitor_configuration.get('monitor', 'service')] = service
                #print(__file__ + ' (57): ' + str(services))
            #else:
            # do some logging

            #except ModuleNotFoundError as err:
            #    raise Exception('something went wrong when initializing a service. you are '
            #                    'using an unknown service in your monitor configuration '
            #                    'identified by: ' + identifier + '({0})'.format(err))

            #service.execute(self)

        if self.__monitor_configuration.get('monitor', 'notifications'):
            for notification_option in self.__monitor_configuration.get('monitor',
                                                                        'notifications').split(','):

                #print(__file__ + ' (72): ' + str(notification_option))
                notification_package = 'linspector.notifications.' + notification_option.lower()
                notification_module = importlib.import_module(notification_package)

                notification = getattr(notification_module, notification_option + 'Notification')
                notification.__init__(self, configuration, environment)

                if notification_option not in notifications:
                    notifications[notification_option] = notification
                    #print(__file__ + ' (81): ' + str(notifications))

    def get_identifier(self):
        return self.__identifier

    # currently only used for testing but maybe i will add get functions for all known variables.
    # but not all variables can be known because all monitors are different. only the service
    # implementation can know all variables which are being used inside the service.
    def get_service(self):
        return self.__monitor_configuration.get('monitor', 'service')
