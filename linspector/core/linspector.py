"""
This file is part of Linspector (https://linspector.org/)
Copyright (c) 2022 Johannes Findeisen <you@hanez.org>. All Rights Reserved.
See LICENSE (MIT license)
"""
import datetime
import importlib
import random

from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.jobstores.memory import MemoryJobStore
from apscheduler.executors.pool import ThreadPoolExecutor, ProcessPoolExecutor

from linspector.core.helpers import log


def job_function(monitor):
    log('debug', __name__, monitor)
    monitor.handle_call()


class Linspector:

    def __init__(self, configuration, environment, monitors, plugins, scheduler):
        self.__configuration = configuration
        self.__environment = environment
        self.__jobs = []
        self.__monitors = monitors
        self.__plugin_list = None
        self.__plugins = plugins
        self.__scheduler = scheduler

        # load plugins
        log('info', __name__, 'loading plugins...')
        if configuration.get_option('linspector', 'plugins'):
            plugin_list = configuration.get_option('linspector', 'plugins')
            self.__plugin_list = plugin_list.split(',')
            for plugin_option in plugin_list.split(','):
                if plugin_option not in plugins:
                    log('info', __name__, 'loading plugin: ' + plugin_option)
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

        start_date = datetime.datetime.now()
        log('debug', __name__, monitors.get_monitors())
        monitors = self.__monitors.get_monitors()
        for monitor in monitors:
            log('debug', __name__, monitor)
            if configuration.get_option('linspector', 'delta_range'):
                time_delta = round(random.uniform(0.00, float(configuration.get_option('linspector', 'delta_range'))), 2)
            else:
                time_delta = round(random.uniform(0.00, 60.00), 2)

            new_start_date = start_date + datetime.timedelta(seconds=time_delta)
            monitor_job = monitors.get(monitor)
            interval = monitor_job.get_interval()
            scheduler_job = scheduler['linspector'].add_job(job_function, 'interval',
                                                            start_date=new_start_date,
                                                            seconds=interval, timezone="CET",
                                                            args=[monitors.get(monitor)])

            monitor_job.set_job(scheduler_job)
            self.__jobs.append(monitor_job)
            log('info', __name__, 'scheduling job ' + monitor + ' with delta ' + str(time_delta) +
                ' @' + str(new_start_date) + ' running service ' + monitor_job.get_service())

        if configuration.get_option('linspector', 'start_scheduler') == 'true':
            self.__scheduler['linspector'].start()

    # this function is just for testing purposes and can be removed some day
    def print_debug(self):
        # example on how to access the monitor objects in monitors
        monitors = self.__monitors.get_monitors()
        print(__file__ + ' (78): ' + str(monitors))
        for monitor in monitors:
            print(__file__ + ' (80): ' + monitors.get(monitor).get_identifier())
            print(__file__ + ' (81): ' + monitors.get(monitor).get_service())
