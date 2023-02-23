"""
This file is part of Linspector (https://linspector.org/)
Copyright (c) 2022 Johannes Findeisen <you@hanez.org>. All Rights Reserved.
See LICENSE (MIT license).
"""
import socket

from linspector.service import Service


def create(configuration, environment, log):
    return PortService(configuration, environment, log)


class PortService(Service):
    def __init__(self, configuration, environment, log):
        super().__init__(configuration, environment, log)
        self.__configuration = configuration
        self.__environment = environment
        self.__log = log

    def execute(self, execution, **kwargs):

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
