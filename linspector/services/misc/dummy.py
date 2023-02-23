"""
This file is part of Linspector (https://linspector.org/)
Copyright (c) 2022 Johannes Findeisen <you@hanez.org>. All Rights Reserved.
See LICENSE (MIT license).
"""
from linspector.service import Service


def create(configuration, environment, log):
    return DummyService(configuration, environment, log)


class DummyService(Service):
    def __init__(self, configuration, environment, log):
        super().__init__(configuration, environment, log)
        self.__configuration = configuration
        self.__environment = environment
        self.__log = log

    def execute(self, **kwargs):
        self.__log.debug('DummyService object ' + str(self) + ' using kwargs: ' + str(kwargs))
        # log('debug', 'dummy object @' + str(self) + str(self.__kwargs['foo']))
        return
