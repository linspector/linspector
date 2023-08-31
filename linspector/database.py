"""
This file is part of Linspector (https://linspector.org/)
Copyright (c) 2013-2023 Johannes Findeisen <you@hanez.org>. All Rights Reserved.
See LICENSE.
"""


class Database:
    def __init__(self, configuration, environment, log):
        self._configuration = configuration
        self._environment = environment
        self._log = log
