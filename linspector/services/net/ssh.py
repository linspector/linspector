"""
This file is part of Linspector (https://linspector.org/)
Copyright (c) 2022 Johannes Findeisen <you@hanez.org>. All Rights Reserved.
See LICENSE.txt (MIT license).
"""
import os
import paramiko
import pprint

from linspector.core.service import Service


def create(configuration, environment, log):
    return SSHService(configuration, environment, log)


class SSHService(Service):
    def __init__(self, configuration, environment, log):
        super().__init__(configuration, environment, log)
        self.__configuration = configuration
        self.__environment = environment
        self.__log = log

    def execute(self, **kwargs):
        path = os.path.join(os.environ['HOME'], '.ssh', 'id_rsa')
        key = paramiko.RSAKey.from_private_key_file(path)

        client = paramiko.SSHClient()
        client.get_host_keys().add('hanez.org', 'ssh-rsa', key)
        pprint.pprint(client._host_keys)

        client.connect('hanez.org', username='hanez')

        #self.command.call() ist dann das:
        stdin, stdout, stderr = client.exec_command('ls')
        for line in stdout:
            print('... ' + line.strip('\n'))
        client.close()

