"""
This file is part of Linspector (https://linspector.org/)
Copyright (c) 2013-2023 Johannes Findeisen <you@hanez.org>. All Rights Reserved.
See LICENSE.
"""

class Task:
    def __init__(self, configuration, environment, log, **kwargs):
        self._args = {}
        self._configuration = configuration
        self._environment = environment
        self._log = log
