"""
This file is part of Linspector (https://linspector.org/)
Copyright (c) 2022-2023 Johannes Findeisen <you@hanez.org>. All Rights Reserved.
See LICENSE (MIT license).
"""
from linspector.database import Database


def create(configuration, environment, log):
    return DummyDBDatabase(configuration, environment, log)


class DummyDBDatabase(Database):
    """
    This is a dummy database
    """

    def connect(self):
        pass

    def insert(self):
        pass
