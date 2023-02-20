"""
This file is part of Linspector (https://linspector.org/)
Copyright (c) 2022 Johannes Findeisen <you@hanez.org>. All Rights Reserved.
See LICENSE.txt (MIT license).
"""
from linspector.core.service import Service


def create(configuration, environment, log):
    return HTTPConnectService(configuration, environment, log)


# Get the status code returned by a http request. Action handling is configured using kwargs. So,
# let's say all below 4** are no errors and others are an error. Or maybe define ranges, or just
# maybe the status code that produces an error.
class HTTPConnectService(Service):
    def __init__(self, configuration, environment, log):
        super().__init__(configuration, environment, log)
        self.__configuration = configuration
        self.__environment = environment
        self.__log = log

    def execute(self, **kwargs):
        return
