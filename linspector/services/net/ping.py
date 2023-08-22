"""
This file is part of Linspector (https://linspector.org/)
Copyright (c) 2013-2023 Johannes Findeisen <you@hanez.org>. All Rights Reserved.
See LICENSE.
"""

from linspector.service import Service


def create(configuration, environment, log):
    return PingService(configuration, environment, log)


class PingService(Service):

    def execute(self, **kwargs):
        return
