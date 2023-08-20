"""
This file is part of Linspector (https://linspector.org/)
Copyright (c) 2022-2023 Johannes Findeisen <you@hanez.org>. All Rights Reserved.
See LICENSE (MIT license).
"""


class Environment:
    """
    Object for storing environment variables at runtime. These variables must not affect the
    stability or runtime of Linspector.
    """

    def __init__(self, log):
        self._env = {}
        self._log = log

    def get_env_var(self, key):
        if key in self._env:
            return self._env[key]
        else:
            self._log.warning('environment var "' + key + '" not found! could be that it is '
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
        if self._env[key]:
            self._log('warning', __name__, 'environment var "' + key +
                      ' existed and was overwritten!')

        self._env[key] = value
