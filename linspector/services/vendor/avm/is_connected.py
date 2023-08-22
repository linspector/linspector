"""
This file is part of Linspector (https://linspector.org/)
Copyright (c) 2013-2023 Johannes Findeisen <you@hanez.org>. All Rights Reserved.
See LICENSE.
"""

from fritzconnection.lib.fritzstatus import FritzStatus

from linspector.service import Service


def create(configuration, environment, log):
    return IsConnectedService(configuration, environment, log)


class IsConnectedService(Service):

    def execute(self, identifier, monitor, service, **kwargs):

        self._log.debug('identifier=' + identifier +
                        ' service=' + service +
                        ' object=' + str(self) +
                        ' kwargs=' + str(kwargs))
        try:
            fc = FritzStatus(address=monitor.get_host(),
                             password=kwargs['password'])
        except Exception as err:
            self._log.error('identifier=' + identifier +
                            ' host=' + monitor.get_host() +
                            ' service=' + service +
                            ' error=' + str(err))
            return {"status": 'ERROR', "message": str(err)}

        self._log.info('identifier=' + identifier +
                       ' host=' + monitor.get_host() +
                       ' service=' + service +
                       ' status=' + ('OK' if fc.is_connected else 'ERROR'))

        result = {"host": monitor.get_host(),
                  "message": "Uplink on host " + monitor.get_host() + " " +
                             ('UP' if fc.is_connected else 'DOWN'),
                  "service": service,
                  "status": ('OK' if fc.is_connected else 'ERROR')}

        return result
