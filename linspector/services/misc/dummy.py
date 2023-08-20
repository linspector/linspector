"""
This file is part of Linspector (https://linspector.org/)
Copyright (c) 2022 Johannes Findeisen <you@hanez.org>. All Rights Reserved.
See LICENSE (MIT license).
"""
from linspector.service import Service


def create(configuration, environment, log):
    return DummyService(configuration, environment, log)


class DummyService(Service):
    """
    This is a dummy service which is doing nothing but logging. It will be used if some other
    service fails at load / configuration, or it can be used for testing.
    """

    def execute(self, identifier, monitor, service, **kwargs):
        self._log.info('identifier=' + identifier +
                       ' host=' + monitor.get_host() +
                       ' service=' + service +
                       ' status=' + 'OK')
        return True
