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

        try:
            fc = FritzStatus(address=monitor.get_host(),
                             user=kwargs['user'],
                             password=kwargs['password'],
                             timeout=10)
            error = 'None'
            if fc.is_connected:
                status = 'OK'
            else:
                status = 'ERROR'
        except Exception as err:
            error = str(err)
            status = 'ERROR'

        result = {'error': error.replace('\'', ''),
                  'host': monitor.get_host(),
                  'log': self.get_str(identifier, monitor.get_host(), service, status),
                  'service': service,
                  'status': status}

        return result
