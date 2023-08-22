"""
This file is part of Linspector (https://linspector.org/)
Copyright (c) 2013-2023 Johannes Findeisen <you@hanez.org>. All Rights Reserved.
See LICENSE.
"""

from linspector.database import Database


def create(configuration, environment, log):
    return DummyDBDatabase(configuration, environment, log)


class DummyDBDatabase(Database):
    """
    This is a dummy database module to make sure all monitors can work without errors even when no
    database is configured. It should always be loaded or only if no other database is selected.
    """

    def insert(self, host, identifier, json, message, service, status, timestamp):
        pass
