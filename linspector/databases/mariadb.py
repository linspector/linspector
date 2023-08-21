"""
This file is part of Linspector (https://linspector.org/)
Copyright (c) 2022-2023 Johannes Findeisen <you@hanez.org>. All Rights Reserved.
See LICENSE (MIT license).
"""
from linspector.database import Database


def create(configuration, environment, log):
    return MariaDBDatabase(configuration, environment, log)


class MariaDBDatabase(Database):

    def execute(self):
        self._log.debug("Hello from MariaDB Database...")
