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
            error = 'None'
            status = 'OK'

        except Exception as err:
            error = str(err)
            status = 'ERROR'

        return {'error': error,
                'host': monitor.get_host(),
                'message': self.get_str(identifier, monitor.get_host(), service, status),
                'service': service,
                'status': status}
