"""
This file is part of Linspector (https://linspector.org/)
Copyright (c) 2013-2023 Johannes Findeisen <you@hanez.org>. All Rights Reserved.
See LICENSE.
"""

# TODO: Make this a backend API using the modern FastAPI framework as a replacement for the
#  traditional RPC plugin. Maybe it makes sense to maintain the RPC plugin too for simple usage by
#  the Lish but I believe it makes sense to only create one backend for all clients.
from linspector.plugin import Plugin


def create(configuration, environment, linspector, log):
    return APIPlugin(configuration, environment, linspector, log)


# TODO: check for all required configuration options and set defaults if needed.
class APIPlugin(Plugin):
    def __init__(self, configuration, environment, linspector, log):
        super().__init__(configuration, environment, linspector, log)
        self._configuration = configuration
        self._environment = environment
        self._linspector = linspector
        self._log = log

    def run(self):
        return
