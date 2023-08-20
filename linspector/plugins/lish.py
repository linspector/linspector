"""
This file is part of Linspector (https://linspector.org/)
Copyright (c) 2022 Johannes Findeisen <you@hanez.org>. All Rights Reserved.
See LICENSE (MIT license).
"""
# TODO: This plugin should become the internal Lish implemented as a plugin which does not use the
#  API plugin but loads at the end when starting Linspector in interactive mode as a terminal like
#  interface to the core of Linspector.
from linspector.plugin import Plugin


def create(configuration, environment, linspector, log):
    return LishPlugin(configuration, environment, linspector, log)


# TODO: check for all required configuration options and set defaults if needed.
class LishPlugin(Plugin):
    def __init__(self, configuration, environment, linspector, log):
        super().__init__(configuration, environment, linspector, log)
        self._configuration = configuration
        self._environment = environment
        self._linspector = linspector
        self._log = log

    def run(self):
        return
