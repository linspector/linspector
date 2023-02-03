"""
This file is part of Linspector (https://linspector.org/)
Copyright (c) 2022 Johannes Findeisen <you@hanez.org>. All Rights Reserved.
See LICENSE (MIT license)
"""
import logging
import os
import sys

from logging import getLogger
from logging import handlers

logger = getLogger('linspector')


# wow, this is not process capable! i thought in a last commit that the problem ist fixed, but it
# isn't!!! see here for more details:
# https://docs.python.org/3/howto/logging-cookbook.html#logging-to-a-single-file-from-multiple-processes
# i think the native pythonic way should be used as described in the link above.
# a different approach on handling this can be to use a exclusive log file for each process but
# this is not what i want. maybe these links could be helpful too:
# https://pypi.org/project/multiprocessing-logging/
# https://stackoverflow.com/questions/641420/how-should-i-log-while-using-multiprocessing-in-python/48668567
# or i can log to one single file using stdout data and let the operating system do the file
# rotation but if the pythonic way works fine i should implement it directly in Linspector.
# more stuff:
# https://pythondjangorestapi.com/python-logging-the-ultimate-guide-to-logging/
# and now i found another libray for handling this, but it would make Linspector depending on the
# next 3rd party library in the core (need to discover features because i want log rotating):
# https://pypi.org/project/loguru/
# maybe subclass it from logging.Logger...?
# TODO: Make the logging format using key=value pairs to make it easy to evaluate log data using
#  Splunk.
# TODO: Make logging possible to syslog! Maybe not implement it here and just use the syslog task
#  with a format optimized for Splunk or create a Splunk task for this.
class Log:
    def __init__(self, configuration, stdout, verbose):
        self.__configuration = configuration
        self.__stdout = stdout
        self.__verbose = verbose

        if stdout:
            if verbose:
                self.set_level(logging.DEBUG)
            else:
                # setting pre initialization default log level to INFO. this changes after
                # initialization of the configuration. maybe there are better solutions...?
                self.set_level(logging.INFO)

            # some information but not sure if useful in Linspector:
            # https://stackoverflow.com/questions/919897/how-to-obtain-a-thread-id-in-python
            # %(thread)d : Thread ID (if available).
            # %(threadName)s : Thread name (if available).
            # this works also for processName
            stdout_formatter = logging.Formatter('[%(asctime)s] [%(levelname)s] [%(name)s] '
                                                 '%(message)s')
            stdout_handler = logging.StreamHandler(sys.stdout)
            stdout_handler.setFormatter(stdout_formatter)
            self.add_handler(stdout_handler)

        if configuration.get_option('linspector', 'log_file'):
            log_file = os.path.expanduser(configuration.get_option('linspector', 'log_file'))
            if not os.path.exists(os.path.dirname(log_file)):
                os.makedirs(os.path.dirname(log_file))

            log_file_formatter = \
                logging.Formatter('[%(asctime)s]:[%(levelname)s]:[%(name)s]:%(message)s')

            if configuration.get_option('linspector', 'log_file_size'):
                log_file_size_mb = int(configuration.get_option('linspector', 'log_file_size'))
                log_file_size_bytes = int(log_file_size_mb * 1000000)
            elif configuration.get_option('linspector', 'log_file_size_bytes'):
                log_file_size_bytes = int(configuration.get_option('linspector',
                                                                   'log_file_size_bytes'))
            else:
                # default log file size is 10000000 bytes (10MiB)
                log_file_size_bytes = int(10000000)

            if configuration.get_option('linspector', 'log_file_count'):
                log_file_count = int(configuration.get_option('linspector', 'log_file_count'))
            else:
                # default log file count is 1.
                log_file_count = 1

            log_file_handler = logging.handlers.RotatingFileHandler(log_file,
                                                                    maxBytes=log_file_size_bytes,
                                                                    backupCount=log_file_count)

            log_file_handler.setFormatter(log_file_formatter)
            self.add_handler(log_file_handler)

        log_level = 'None'
        # critical errors will always show up even when no log_level is set. this is most silent.
        self.set_level(logging.CRITICAL)
        if configuration.get_option('linspector', 'log_level'):
            log_level = str(configuration.get_option('linspector', 'log_level'))
            if log_level == "error":
                self.set_level(logging.ERROR)
            elif log_level == "warning":
                self.set_level(logging.WARNING)
            elif log_level == "info":
                self.set_level(logging.INFO)
            elif log_level == "debug":
                self.set_level(logging.DEBUG)
            #elif configuration.get_option('linspector', 'log_level') != 'error' != 'warning' \
            #        != 'info' != 'debug':
            #    logger.warning('[linspector] log level: "' + log_level + '" not found!')

    @staticmethod
    def add_handler(handler):
        logger.addHandler(handler)

    @staticmethod
    def critical(msg):
        logger.critical(str(msg))

    @staticmethod
    def debug(msg):
        # only use inspect when log level NOTSET or DEBUG  is enabled.
        if logger.isEnabledFor(0) or logger.isEnabledFor(10):
            import inspect
            import multiprocessing
            import threading
            # https://www.geeksforgeeks.org/how-to-get-the-process-id-from-python-multiprocess/
            current_process = multiprocessing.current_process()
            from_stack = inspect.stack()[1]
            function_name = from_stack.function
            line_number = str(from_stack.lineno)
            module_name = inspect.getmodule(from_stack[0]).__name__
            logger.debug('[' + str(current_process.name) + ']:[' + str(threading.get_ident()) +
                         ']:[' + str(threading.get_native_id()) + '] [' + module_name + ']:[' +
                         function_name + ']:[' + line_number + '] ' + str(msg))

    @staticmethod
    def error(msg):
        logger.error(str(msg))

    @staticmethod
    def info(msg):
        logger.info(str(msg))

    @staticmethod
    def warning(msg):
        logger.warning(str(msg))

    @staticmethod
    def set_level(level):
        logger.setLevel(level)
