"""
This file is part of Linspector (https://linspector.org/)
Copyright (c) 2022 Johannes Findeisen <you@hanez.org>. All Rights Reserved.
See LICENSE (MIT license)
"""
from logging import getLogger

logger = getLogger('linspector')


def log(level, msg):
    # only use inspect when log level NOTSET or DEBUG  is enabled.
    if logger.isEnabledFor(0) or logger.isEnabledFor(10):
        import inspect
        from_stack = inspect.stack()[1]
        function_name = from_stack.function
        line_number = str(from_stack.lineno)
        module_name = inspect.getmodule(from_stack[0]).__name__
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
    else:
        if level == 'critical':
            logger.critical(str(msg))
        if level == 'error':
            logger.error(str(msg))
        elif level == 'warning':
            logger.warning(str(msg))
        elif level == 'info':
            logger.info(str(msg))
        elif level == 'debug':
            logger.debug(str(msg))
