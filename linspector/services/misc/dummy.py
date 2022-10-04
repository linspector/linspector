"""
This file is part of Linspector (https://linspector.org/)
Copyright (c) 2022 Johannes Findeisen <you@hanez.org>. All Rights Reserved.
See LICENSE (MIT license)
"""
from linspector.core.helpers import log
from linspector.core.service import Service


def create(configuration, environment):
    return DummyService(configuration, environment)


class DummyService(Service):

    def __init__(self, configuration, environment):
        super().__init__(configuration, environment)
        self.__configuration = configuration
        self.__environment = environment

    def execute(self, **kwargs):
        log('debug', 'DummyService object ' + str(self))
        #log('debug', 'dummy object @' + str(self) + str(self.__kwargs['foo']))
        return
