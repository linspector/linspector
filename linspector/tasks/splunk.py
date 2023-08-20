"""
This file is part of Linspector (https://linspector.org/)
Copyright (c) 2023 Johannes Findeisen <you@hanez.org>. All Rights Reserved.
See LICENSE (MIT license).
"""
from linspector.task import Task


def create(configuration, environment, log):
    return SplunkTask(configuration, environment, log)


# TODO: check for all required configuration options and set defaults if needed.
class SplunkTask(Task):
    def __init__(self, configuration, environment, log):
        super().__init__(configuration, environment, log)
        self._configuration = configuration
        self._environment = environment
        self._log = log
