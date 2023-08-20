"""
This file is part of Linspector (https://linspector.org/)
Copyright (c) 2023 Johannes Findeisen <you@hanez.org>. All Rights Reserved.
See LICENSE (MIT license).
"""
# TODO: Think about this idea it little bit more. Maybe Syslog support should not become a plugin
#  but should better be implemented in the core.
from linspector.plugin import Plugin


def create(configuration, environment, linspector, log):
    return SyslogPlugin(configuration, environment, linspector, log)


# TODO: check for all required configuration options and set defaults if needed.
class SyslogPlugin(Plugin):
    def __init__(self, configuration, environment, linspector, log):
        super().__init__(configuration, environment, linspector, log)
        self._configuration = configuration
        self._environment = environment
        self._linspector = linspector
        self._log = log

    def run(self):
        return
