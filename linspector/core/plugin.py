"""
This file is part of Linspector (https://linspector.org/)
Copyright (c) 2022 Johannes Findeisen <you@hanez.org>. All Rights Reserved.
See LICENSE (MIT license)
"""


class Plugin:
    def __init__(self, configuration, environment, linspector, log):
        self.__configuration = configuration
        self._environment = environment
        self.__linspector = linspector
        self.__log = log
