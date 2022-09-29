"""
This file is part of Linspector (https://linspector.org/)
Copyright (c) 2022 Johannes Findeisen <you@hanez.org>. All Rights Reserved.
See LICENSE (MIT license)
"""
from logging import getLogger

from linspector.core.task import Task

logger = getLogger('linspector')


def get(configuration, environment):
    return CSVTask(configuration, environment)


# TODO: check for all required configuration options and set defaults if needed.
class CSVTask(Task):

    def __init__(self, configuration, environment):
        super().__init__(configuration, environment)
        self.__configuration = configuration
        self.__environment = environment
