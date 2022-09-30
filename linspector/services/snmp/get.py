"""
This file is part of Linspector (https://linspector.org/)
Copyright (c) 2022 Johannes Findeisen <you@hanez.org>. All Rights Reserved.
See LICENSE (MIT license)
"""
from pysnmp.entity.rfc3413.oneliner import cmdgen

from linspector.core.helpers import log
from linspector.core.service import Service


def create(configuration, environment, **kwargs):
    return GetService(configuration, environment, **kwargs)


class GetService(Service):

    def __init__(self, configuration, environment, **kwargs):
        super().__init__(configuration, environment, **kwargs)
        self.__configuration = configuration
        self.__environment = environment
        self.__kwargs = kwargs

    def execute(self):
        return
