"""
This file is part of Linspector (https://linspector.org/)
Copyright (c) 2022 Johannes Findeisen <you@hanez.org>. All Rights Reserved.
See LICENSE (MIT license)
"""
from linspector.core.helpers import log
from linspector.core.service import Service


def create(configuration, environment, **kwargs):
    return DummyService(configuration, environment, **kwargs)


class DummyService(Service):

    def __init__(self, configuration, environment, **kwargs):
        super().__init__(configuration, environment)
        self.__configuration = configuration
        self.__environment = environment
        self.__kwargs = kwargs

    def execute(self):
        log('debug', __name__, 'dummy object @' + str(self) + str(self.__kwargs['foo']))
        return
