"""
This file is part of Linspector (https://linspector.org/)
Copyright (c) 2013-2023 Johannes Findeisen <you@hanez.org>. All Rights Reserved.
See LICENSE.
"""

from linspector.service import Service


def create(configuration, environment, log):
    return HTTPConnectService(configuration, environment, log)


# Get the status code returned by a http request. Action handling is configured using kwargs. So,
# let's say all below 4** are no errors and others are an error. Or maybe define ranges, or just
# maybe the status code that produces an error.
class HTTPConnectService(Service):

    def execute(self, **kwargs):
        return
