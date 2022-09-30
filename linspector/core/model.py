"""
This file is part of Linspector (https://linspector.org/)
Copyright (c) 2022 Johannes Findeisen <you@hanez.org>. All Rights Reserved.
See LICENSE (MIT license)
"""
from linspector.core.helpers import log


# This class can maybe be used for a general data model for Linspector data processing. currently
# the is no use for it and no place known where it could be used with sense.
class Model:

    def __init__(self, configuration, environment):
        self.__configuration = configuration
        self._environment = environment
