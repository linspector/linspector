"""
This file is part of Linspector (https://linspector.org/)
Copyright (c) 2022 Johannes Findeisen <you@hanez.org>. All Rights Reserved.
See LICENSE (MIT license).
"""


class Notification:
    def __init__(self, configuration, environment, log):
        super().__init__()
        self.__configuration = configuration
        self.__environment = environment
        self.__log = log
