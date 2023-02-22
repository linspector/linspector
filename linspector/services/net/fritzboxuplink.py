"""
This file is part of Linspector (https://linspector.org/)
Copyright (c) 2022 Johannes Findeisen <you@hanez.org>. All Rights Reserved.
See LICENSE.txt (MIT license).
"""
from fritzconnection.lib.fritzstatus import FritzStatus

from linspector.core.service import Service


def create(configuration, environment, log):
    return FritzboxUplinkService(configuration, environment, log)


class FritzboxUplinkService(Service):
    def __init__(self, configuration, environment, log):
        super().__init__(configuration, environment, log)
        self.__configuration = configuration
        self.__environment = environment
        self.__log = log

    def execute(self, identifier, service, **kwargs):
        status = "NONE"
        self.__log.debug('identifier=' + identifier +
                         'service=' + service +
                         ' object=' + str(self) +
                         ' kwargs=' + str(kwargs))
        try:
            fc = FritzStatus(address=kwargs['host'],
                             password=kwargs['password'])

            if fc.is_connected:
                status = "OK"
            else:
                status = "ERROR"
        except Exception:
            self.__log.error('identifier=' + identifier +
                             ' host=' + str(kwargs['host']) +
                             ' service=' + service +
                             ' failed ')
            return False

        self.__log.info('identifier=' + identifier +
                        ' host=' + str(kwargs['host']) +
                        ' service=' + service +
                        ' status=' + status)
        return True
