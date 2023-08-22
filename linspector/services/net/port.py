"""
This file is part of Linspector (https://linspector.org/)
Copyright (c) 2013-2023 Johannes Findeisen <you@hanez.org>. All Rights Reserved.
See LICENSE.
"""

import socket

from linspector.service import Service


def create(configuration, environment, log):
    return PortService(configuration, environment, log)


class PortService(Service):

    def execute(self, identifier, monitor, service, **kwargs):

        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.connect((monitor.get_host(), int(kwargs['port'])))
            sock.close()

            self._log.info('Connection to host ' + monitor.get_host() + ' on port ' +
                           kwargs['port'] + ' successful')

            return {'status': 'OK',
                    'message': 'Connection to host ' + monitor.get_host() + ' on port ' +
                               kwargs['port'] + ' successful', 'host': monitor.get_host(),
                    'service': service}

        except Exception as err:
            self._log.info('Connection to host ' + monitor.get_host() + ' on port ' +
                           kwargs['port'] + ' failed (' + str(err))

            return {'status': 'ERROR',
                    'message': 'Connection to host ' + monitor.get_host() + ' on port ' +
                               kwargs['port'] + ' failed (' + str(err) +
                               ')', 'host': monitor.get_host(),
                    'service': service}

