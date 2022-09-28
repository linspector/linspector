"""
This file is part of Linspector (https://linspector.org/)
Copyright (c) 2022 Johannes Findeisen <you@hanez.org>. All Rights Reserved.
See LICENSE (MIT license)
"""
from logging import getLogger

logger = getLogger('linspector')


# The logger can be used by any monitor to write arbitrary data to any arbitrary place.
# Need to think about this more but some monitors are or can collect more data than needed for
# running monipyd. This enables longtime storage of collected data like in uplink.
# Maybe this can be archived by storing an arbitrary JSON string in a none defined field in the
# database. then maybe redis can be used for everything. Storing data should be optional for
# running monipyd.
class Logger:

    def __init__(self, configuration, environment):
        self.__configuration = configuration
        self.__environment = environment
