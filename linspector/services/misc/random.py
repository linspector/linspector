"""
This file is part of Linspector (https://linspector.org/)
Copyright (c) 2022 Johannes Findeisen <you@hanez.org>. All Rights Reserved.
See LICENSE (MIT license).
"""
import hashlib
import random

from linspector.service import Service


def create(configuration, environment, log):
    return DummyService(configuration, environment, log)


class DummyService(Service):
    """
    This is a service that produces random data and status results. It is only used for testing.
    """
    def __init__(self, configuration, environment, log):
        super().__init__(configuration, environment, log)
        self.__configuration = configuration
        self.__environment = environment
        self.__log = log

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
        sha512_1 = hashlib.sha512(str((str(rnd1) + str(rnd2) + str(rnd3) + str(rnd4) +
                                  str(rnd5) + str(rnd6) + str(rnd7) + str(rnd8))).
                                  encode('utf-8')).hexdigest()
        sha512_2 = hashlib.sha512(str((str(rnd1) + str(rnd2) + str(rnd3) + str(rnd4) +
                                  str(rnd5) + str(rnd6) + str(rnd7) + str(rnd8) + str(sha512_1))).
                                  encode('utf-8')).hexdigest()
        self.__log.info('identifier=' + identifier +
                        ' host=' + monitor.get_host() +
                        ' service=' + service +
                        ' status=' + ('OK' if status == 0 else 'ERROR') + ' sha512=' +
                        sha512_2)
        return True
