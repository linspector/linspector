"""
This file is part of Linspector (https://linspector.org/)
Copyright (c) 2022 Johannes Findeisen <you@hanez.org>. All Rights Reserved.
See LICENSE (MIT license).
"""
import os
import pprint

import paramiko

from linspector.service import Service


def create(configuration, environment, log):
    return SSHService(configuration, environment, log)


class SSHService(Service):

    def execute(self, **kwargs):
        path = os.path.join(os.environ['HOME'], '.ssh', 'id_rsa')
        key = paramiko.RSAKey.from_private_key_file(path)

        client = paramiko.SSHClient()
        client.get_host_keys().add('hanez.org', 'ssh-rsa', key)
        pprint.pprint(client._host_keys)

        client.connect('hanez.org', username='hanez')

        # self.command.call() ist dann das:
        stdin, stdout, stderr = client.exec_command('ls')
        for line in stdout:
            print('... ' + line.strip('\n'))
        client.close()
