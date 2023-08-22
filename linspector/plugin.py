"""
This file is part of Linspector (https://linspector.org/)
Copyright (c) 2013-2023 Johannes Findeisen <you@hanez.org>. All Rights Reserved.
See LICENSE.
"""

class Plugin:
    def __init__(self, configuration, environment, linspector, log):
        self._configuration = configuration
        self._environment = environment
        self._linspector = linspector
        self._log = log
