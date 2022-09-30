"""
This file is part of Linspector (https://linspector.org/)
Copyright (c) 2022 Johannes Findeisen <you@hanez.org>. All Rights Reserved.
See LICENSE (MIT license)
"""
from logging import getLogger

logger = getLogger('linspector')


def log(level, name, msg):
    if level == 'critical':
        logger.critical('[' + name + '] ' + str(msg))
    if level == 'error':
        logger.error('[' + name + '] ' + str(msg))
    elif level == 'warning':
        logger.warning('[' + name + '] ' + str(msg))
    elif level == 'info':
        logger.info('[' + name + '] ' + str(msg))
    elif level == 'debug':
        logger.debug('[' + name + '] ' + str(msg))
