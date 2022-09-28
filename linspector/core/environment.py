"""
This file is part of Linspector (https://linspector.org/)
Copyright (c) 2022 Johannes Findeisen <you@hanez.org>. All Rights Reserved.
See LICENSE (MIT license)
"""
from logging import getLogger

logger = getLogger('linspector')


class Environment:
    """
    Object for storing environment variables at runtime. These variables must not affect the
    stability or runtime of Linspector.
    """
    def __init__(self):
        self.__env = {}

    def get_env_var(self, key):
        if key in self.__env:
            return self.__env[key]
        else:
            logger.info('environment var "' + key + '" not found! could be that it is set later at '
                                                    'runtime. if you encounter any errors '
                                                    'executing monipyd, something is wrong in the '
                                                    'logic of the code. please consider reporting '
                                                    'this as a bug! btw. INFO is not an ERROR! '
                                                    'monipyd should work even with missing '
                                                    'environment variables.')
            return None

    def set_env_var(self, key, value):
        if self.__env[key]:
            logger.warning('environment var "' + key + ' existed and was overwritten!')

        self.__env[key] = value
