"""
This file is part of Linspector (https://linspector.org/)
Copyright (c) 2022 Johannes Findeisen <you@hanez.org>. All Rights Reserved.
See LICENSE (MIT license)
"""
from logging import getLogger

logger = getLogger('linspector')


class Plugin:

    def __init__(self, configuration, environment, linspector):
        self.__configuration = configuration
        self._environment = environment
        self.__linspector = linspector
