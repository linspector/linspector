"""
This file is part of Linspector (https://linspector.org/)
Copyright (c) 2022 Johannes Findeisen <you@hanez.org>. All Rights Reserved.
See LICENSE (MIT license).
"""
import hashlib
import random

from linspector.service import Service


def create(configuration, environment, log):
    return RandomService(configuration, environment, log)


class RandomService(Service):
    """
    This is a service that produces random data and status results. It is only used for testing.
    """

    def execute(self, identifier, monitor, service, **kwargs):
        status = random.randint(0, 1)
        rnd1 = random.randint(0, 99999999999999)
        rnd2 = random.randint(0, 99999999999999)
        rnd3 = random.randint(0, 99999999999999)
        rnd4 = random.randint(0, 99999999999999)
        rnd5 = random.randint(0, 99999999999999)
        rnd6 = random.randint(0, 99999999999999)
        rnd7 = random.randint(0, 99999999999999)
        rnd8 = random.randint(0, 99999999999999)
        sha256 = hashlib.sha256(str((str(rnd1) + str(rnd2) + str(rnd3) + str(rnd4) +
                                str(rnd5) + str(rnd6) + str(rnd7) + str(rnd8))).
                                encode('utf-8')).hexdigest()
        sha512 = hashlib.sha512(str((str(rnd1) + str(rnd2) + str(rnd3) + str(rnd4) +
                                str(rnd5) + str(rnd6) + str(rnd7) + str(rnd8) + str(sha256))).
                                encode('utf-8')).hexdigest()
        self._log.info('identifier=' + identifier +
                       ' host=' + monitor.get_host() +
                       ' service=' + service +
                       ' status=' + ('OK' if status == 0 else 'ERROR') + ' message=' +
                       sha512)

        result = {"status": ('OK' if status == 0 else 'ERROR'), "message": sha512}

        return result
