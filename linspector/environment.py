"""
This file is part of Linspector (https://linspector.org/)
Copyright (c) 2022 Johannes Findeisen <you@hanez.org>. All Rights Reserved.
See LICENSE (MIT license).
"""


class Environment:
    """
    Object for storing environment variables at runtime. These variables must not affect the
    stability or runtime of Linspector.
    """

    def __init__(self, log):
        self.__env = {}
        self.__log = log

    def get_env_var(self, key):
        if key in self.__env:
            return self.__env[key]
        else:
            self.__log.warning('environment var "' + key + '" not found! could be that it is '
                                                           'set later at runtime. if you '
                                                           'encounter any errors executing '
                                                           'linspector, something is wrong '
                                                           'in the logic of the code. please '
                                                           'consider reporting this as a '
                                                           'bug! btw. a WARNING is not an '
                                                           'ERROR! linspector should work '
                                                           'even with missing environment '
                                                           'variables.')
            return None

    def set_env_var(self, key, value):
        if self.__env[key]:
            self.__log('warning', __name__, 'environment var "' + key +
                       ' existed and was overwritten!')

        self.__env[key] = value
