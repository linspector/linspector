"""
This file is part of Linspector (https://linspector.org/)
Copyright (c) 2022 Johannes Findeisen <you@hanez.org>. All Rights Reserved.
See LICENSE (MIT license).
"""
from linspector.task import Task


def create(configuration, environment, log):
    return CSVTask(configuration, environment, log)


# TODO: check for all required configuration options and set defaults if needed.
class CSVTask(Task):
    def __init__(self, configuration, environment, log):
        super().__init__(configuration, environment, log)
        self._configuration = configuration
        self._environment = environment
        self._log = log

    def execute(self):
        print("Hello from CSV Task...")
