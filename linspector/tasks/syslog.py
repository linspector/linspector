"""
This file is part of Linspector (https://linspector.org/)
Copyright (c) 2013-2023 Johannes Findeisen <you@hanez.org>. All Rights Reserved.
See LICENSE.
"""

from linspector.task import Task


def create(configuration, environment, log):
    return SyslogTask(configuration, environment, log)


# TODO: check for all required configuration options and set defaults if needed.
class SyslogTask(Task):
    def __init__(self, configuration, environment, log):
        super().__init__(configuration, environment, log)
        pass
