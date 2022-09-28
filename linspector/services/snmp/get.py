"""
This file is part of Linspector (https://linspector.org/)
Copyright (c) 2022 Johannes Findeisen <you@hanez.org>. All Rights Reserved.
See LICENSE (MIT license)
"""
from logging import getLogger
from pysnmp.entity.rfc3413.oneliner import cmdgen

from linspector.core.service import Service

logger = getLogger('linspector')


def get(configuration, environment):
    return GetService(configuration, environment)


class GetService(Service):

    def __init__(self, configuration, environment):
        super().__init__(configuration, environment)
        self.__configuration = configuration
        self.__environment = environment

    def execute(self):
        return
