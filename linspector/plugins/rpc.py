"""
This file is part of Linspector (https://linspector.org/)
Copyright (c) 2013-2023 Johannes Findeisen <you@hanez.org>. All Rights Reserved.
See LICENSE.
"""

from linspector.plugin import Plugin


def create(configuration, environment, linspector, log):
    return RPCPlugin(configuration, environment, linspector, log)


# TODO: check for all required configuration options and set defaults if needed.
class RPCPlugin(Plugin):
    def __init__(self, configuration, environment, linspector, log):
        super().__init__(configuration, environment, linspector, log)
        self._configuration = configuration
        self._environment = environment
        self._linspector = linspector
        self._log = log

    def run(self):
        return
