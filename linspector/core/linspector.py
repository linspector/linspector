"""
This file is part of Linspector (https://linspector.org/)
Copyright (c) 2022 Johannes Findeisen <you@hanez.org>. All Rights Reserved.
See LICENSE (MIT license)
"""
import importlib

from logging import getLogger

from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.jobstores.memory import MemoryJobStore
from apscheduler.executors.pool import ThreadPoolExecutor  # , ProcessPoolExecutor

logger = getLogger('linspector')


def job_function(job):
    job.handle_call()


class Linspector:

    def __init__(self, configuration, environment, monitors, plugins, scheduler):
        self.__configuration = configuration
        self.__environment = environment
        self.__monitors = monitors
        self.__plugin_list = None
        self.__plugins = plugins
        self.__scheduler = scheduler

        # load plugins
        logger.info('loading plugins...')
        if configuration.get_option('linspector', 'plugins'):
            plugin_list = configuration.get_option('linspector', 'plugins')
            self.__plugin_list = plugin_list.split(',')
            for plugin_option in plugin_list.split(','):
                if plugin_option not in plugins:
                    logger.info('loading plugin: ' + plugin_option)
                    plugin_package = 'linspector.plugins.' + plugin_option.lower()
                    plugin_module = importlib.import_module(plugin_package)
                    plugin = plugin_module.get(configuration, environment, self)
                    plugins[plugin_option.lower()] = plugin

        jobstores = {
            'memory': MemoryJobStore()
        }
        executors = {
            'default': ThreadPoolExecutor(int(configuration.get_option('linspector',
                                                                       'max_threads'))),
            #'default': ProcessPoolExecutor(int(configuration.get_option('linspector',
            #                                                            'max_processes')))
        }
        job_defaults = {
            'max_instances': 10000
        }
        self.__scheduler['linspector'] = BackgroundScheduler(jobstores=jobstores,
                                                             executors=executors,
                                                             job_defaults=job_defaults)

        if configuration.get_option('linspector', 'start_scheduler') == 'true':
            self.__scheduler['linspector'].start()

    # this function is just for testing purposes and can be removed some day
    def print_debug(self):
        # example on how to access the monitor objects in monitors
        monitors = self.__monitors.get_monitors()
        print(__file__ + ' (59): ' + str(monitors))
        for monitor in monitors:
            print(__file__ + ' (61): ' + monitors.get(monitor).get_identifier())
            print(__file__ + ' (62): ' + monitors.get(monitor).get_service())
