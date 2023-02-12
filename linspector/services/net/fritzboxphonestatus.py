"""
This file is part of Linspector (https://linspector.org/)
Copyright (c) 2022 Johannes Findeisen <you@hanez.org>. All Rights Reserved.
See LICENSE.txt (MIT license).
"""

from linspector.core.service import Service


def create(configuration, environment, log):
    return FritzboxPhoneStatusService(configuration, environment, log)


class FritzboxPhoneStatusService(Service):
    def __init__(self, configuration, environment, log):
        super().__init__(configuration, environment, log)
        self.__configuration = configuration
        self.__environment = environment
        self.__log = log

    def execute(self, **kwargs):
        self.__log.debug('FritzboxPhoneStatusService object ' + str(self))
        return
