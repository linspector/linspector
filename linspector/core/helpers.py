"""
This file is part of Linspector (https://linspector.org/)
Copyright (c) 2022 Johannes Findeisen <you@hanez.org>. All Rights Reserved.
See LICENSE (MIT license)
"""
import inspect

from logging import getLogger

logger = getLogger('linspector')


def log(level, msg):
    frm = inspect.stack()[1]
    function_name = frm.function
    module_name = inspect.getmodule(frm[0]).__name__
    line_number = str(frm.lineno)
    if level == 'critical':
        logger.critical('[' + module_name + ']:[' + function_name + ']:[' + line_number + '] ' +
                        str(msg))
    if level == 'error':
        logger.error('[' + module_name + ']:[' + function_name + ']:[' + line_number + '] ' +
                     str(msg))
    elif level == 'warning':
        logger.warning('[' + module_name + ']:[' + function_name + ']:[' + line_number + '] ' +
                       str(msg))
    elif level == 'info':
        logger.info('[' + module_name + ']:[' + function_name + ']:[' + line_number + '] ' +
                    str(msg))
    elif level == 'debug':
        logger.debug('[' + module_name + ']:[' + function_name + ']:[' + line_number + '] ' +
                     str(msg))
