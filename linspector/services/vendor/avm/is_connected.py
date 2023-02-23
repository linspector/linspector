"""
This file is part of Linspector (https://linspector.org/)
Copyright (c) 2022 Johannes Findeisen <you@hanez.org>. All Rights Reserved.
See LICENSE (MIT license).
"""
from fritzconnection.lib.fritzstatus import FritzStatus

from linspector.service import Service


def create(configuration, environment, log):
    return IsConnectedService(configuration, environment, log)


class IsConnectedService(Service):
    def __init__(self, configuration, environment, log):
        super().__init__(configuration, environment, log)
        self.__configuration = configuration
        self.__environment = environment
        self.__log = log

    def execute(self, identifier, monitor, service, **kwargs):
        self.__log.debug('identifier=' + identifier +
                         'service=' + service +
                         ' object=' + str(self) +
                         ' kwargs=' + str(kwargs))
        try:
            fc = FritzStatus(address=monitor.get_host(),
                             password=kwargs['password'])
        except Exception as err:
            self.__log.error('identifier=' + identifier +
                             ' host=' + monitor.get_host() +
                             ' service=' + service +
                             ' error=' + str(err))
            return False

        self.__log.info('identifier=' + identifier +
                        ' host=' + monitor.get_host() +
                        ' service=' + service +
                        ' status=' + ('OK' if fc.is_connected else 'ERROR'))

        if fc.is_connected:
            return True
        else:
            return False
