"""
This file is part of Linspector (https://linspector.org/)
Copyright (c) 2022 Johannes Findeisen <you@hanez.org>. All Rights Reserved.
See LICENSE (MIT license)
"""
from linspector.core.helpers import log
from linspector.core.task import Task


def create(configuration, environment):
    return FileLoggerTask(configuration, environment)


# TODO: check for all required configuration options and set defaults if needed.
class FileLoggerTask(Task):

    def __init__(self, configuration, environment):
        super().__init__(configuration, environment)
        self.__configuration = configuration
        self.__environment = environment
