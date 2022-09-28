"""
This file is part of Linspector (https://linspector.org/)
Copyright (c) 2022 Johannes Findeisen <you@hanez.org>. All Rights Reserved.
See LICENSE (MIT license)
"""
from logging import getLogger

from linspector.core.plugin import Plugin

logger = getLogger('linspector')


def get(configuration, environment, linspector):
    return LishPlugin(configuration, environment, linspector)


# TODO: check for all required configuration options and set defaults if needed.
class LishPlugin(Plugin):

    def __init__(self, configuration, environment, linspector):
        super().__init__(configuration, environment, linspector)
        self.__configuration = configuration
        self.__environment = environment
        self.__linspector = linspector

    def run(self):
        return
