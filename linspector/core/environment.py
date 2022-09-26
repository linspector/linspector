"""
This file is part of Linspector (https://linspector.org/)
Copyright (c) 2022 Johannes Findeisen <you@hanez.org>

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is furnished
to do so, subject to the following conditions:

The above copyright notice and this permission notice (including the next
paragraph) shall be included in all copies or substantial portions of the
Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS
FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS
OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY,
WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF
OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
"""

from logging import getLogger

logger = getLogger('linspector')


class Environment:
    """
    Object for storing environment variables at runtime. These variables must not affect the
    stability or runtime of Linspector.
    """
    def __init__(self, configuration):
        self.__configuration = configuration

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
            logger.info('environment var "' + key + ' existed and was overwritten.')

        self.__env[key] = value
