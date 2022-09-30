"""
This file is part of Linspector (https://linspector.org/)
Copyright (c) 2022 Johannes Findeisen <you@hanez.org>. All Rights Reserved.
See LICENSE (MIT license)
"""
import socket

from linspector.core.helpers import log
from linspector.core.service import Service


def create(configuration, environment, **kwargs):
    return PortService(configuration, environment, **kwargs)


class PortService(Service):

    def __init__(self, configuration, environment, **kwargs):
        super().__init__(configuration, environment, **kwargs)
        self.__configuration = configuration
        self.__environment = environment
        self.__kwargs = kwargs

    def execute(self, execution):

        error_code = 0
        msg = "Connection successful established"

        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        except socket.error as err:
            error_code = 2
            msg = "Could not create socket"

        try:
            sock.connect((execution.get_host_name(), self.port))
        except socket.error as err:
            error_code = 1
            msg = "Could not establish connection"

        sock.close()
