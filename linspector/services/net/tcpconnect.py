"""
This file is part of Linspector (https://linspector.org/)
Copyright (c) 2022 Johannes Findeisen <you@hanez.org>. All Rights Reserved.
See LICENSE (MIT license).
"""
from linspector.service import Service


def create(configuration, environment, log):
    return TCPConnectService(configuration, environment, log)


# TODO: check for all required configuration options and set defaults if needed.
class TCPConnectService(Service):

    def execute(self, **kwargs):
        return
