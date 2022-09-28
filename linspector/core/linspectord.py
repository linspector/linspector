"""
This file is part of Linspector (https://linspector.org/)
Copyright (c) 2022 Johannes Findeisen <you@hanez.org>. All Rights Reserved.
See LICENSE (MIT license)
"""
from logging import getLogger

from linspector.core.daemon import Daemon

logger = getLogger('linspector')


class Linspectord(Daemon):

    def __init__(self, configuration, environment, linspector):
        super().__init__(configuration.get_option('linspector', 'pid_file'))
        self.__configuration = configuration
        self.__environment = environment
        self.__linspector = linspector

    def run(self):
        return
