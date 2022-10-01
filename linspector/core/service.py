"""
This file is part of Linspector (https://linspector.org/)
Copyright (c) 2022 Johannes Findeisen <you@hanez.org>. All Rights Reserved.
See LICENSE (MIT license)
"""
from linspector.core.helpers import log


class Service:

    def __init__(self, configuration, environment):
        self.__configuration = configuration
        self._environment = environment
