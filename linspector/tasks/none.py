"""
This file is part of Linspector (https://linspector.org/)
Copyright (c) 2013-2023 Johannes Findeisen <you@hanez.org>. All Rights Reserved.
See LICENSE.
"""

# !!! DEPRECATED AND CAN BE REMOVED BECAUSE THERE IS NO NEED ANYMORE !!!

from linspector.task import Task


def create(configuration, environment, log):
    return NoneTask(configuration, environment, log)


class NoneTask(Task):
    """
    This is a dummy task module to make sure all monitors can work without errors even when no
    task is configured. It should always be loaded or only if no other task is selected.
    """

    @staticmethod
    def execute(host, identifier, json, message, service, status, timestamp):
        pass
