"""
This file is part of Linspector (https://linspector.org/)
Copyright (c) 2022 Johannes Findeisen <you@hanez.org>. All Rights Reserved.
See LICENSE (MIT license).
"""


class Notification:
    def __init__(self, configuration, environment, log):
        super().__init__()
        self._configuration = configuration
        self._environment = environment
        self._log = log
