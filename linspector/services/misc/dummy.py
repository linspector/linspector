"""
This file is part of Linspector (https://linspector.org/)
Copyright (c) 2022 Johannes Findeisen <you@hanez.org>. All Rights Reserved.
See LICENSE (MIT license).
"""
from linspector.service import Service


def create(configuration, environment, log):
    return DummyService(configuration, environment, log)


class DummyService(Service):
    """
    This is a dummy service which is doing nothing but logging. It will be used if some other
    service fails at load / configuration, or it can be used for testing.
    """
    def __init__(self, configuration, environment, log):
        super().__init__(configuration, environment, log)
        self.__configuration = configuration
        self.__environment = environment
        self.__log = log

    def execute(self, identifier, monitor, service, **kwargs):
        self.__log.info('identifier=' + identifier +
                        ' host=' + monitor.get_host() +
                        ' service=' + service +
                        ' status=' + 'OK')
        return True
