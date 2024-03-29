"""
This file is part of Linspector (https://linspector.org/)
Copyright (c) 2013-2023 Johannes Findeisen <you@hanez.org>. All Rights Reserved.
See LICENSE.
"""

from linspector.task import Task


def create(configuration, environment, log):
    return FileTask(configuration, environment, log)


# TODO: check for all required configuration options and set defaults if needed.
class FileTask(Task):

    def execute(self):
        self._log.debug("Hello from File Task...")
