"""
This file is part of Linspector (https://linspector.org/)
Copyright (c) 2013-2023 Johannes Findeisen <you@hanez.org>. All Rights Reserved.
See LICENSE.
"""


class Service:
    def __init__(self, configuration, environment, log):
        self._configuration = configuration
        self._environment = environment
        self._log = log

    @staticmethod
    def get_str(identifier, host, service, status):
        log_string = ('identifier=' + identifier +
                      ' host=' + host + ' service=' + service + ' status=' + status)
        return log_string
