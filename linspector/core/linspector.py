"""
This file is part of Linspector (https://linspector.org/)
Copyright (c) 2022 Johannes Findeisen <you@hanez.org>. All Rights Reserved.
See LICENSE.txt (MIT license).
"""
import datetime
import importlib
import random

from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.jobstores.memory import MemoryJobStore
from apscheduler.executors.pool import ThreadPoolExecutor, ProcessPoolExecutor


def job_function(log, monitor):
    try:
        log.debug('executing job_function for monitor identifier: ' + monitor.get_identifier() +
                  ' with monitor object: ' + str(monitor))
        monitor.handle_call()
    except Exception as err:
        log.warning('execution failed for job_function for monitor identifier: ' +
                    monitor.get_identifier() + ' with monitor object: ' + str(monitor) +
                    ' error: ' + str(err))


class Linspector:
    def __init__(self, configuration, environment, log, monitors, plugins, scheduler):
        self.__configuration = configuration
        self.__environment = environment
        self.__jobs = []
        self.__log = log
        self.__monitors = monitors
        self.__plugin_list = []
        self.__plugins = plugins
        self.__scheduler = scheduler

        # load plugins
        log.info('loading plugins...')
        if configuration.get_option('linspector', 'plugins'):
            plugin_list = configuration.get_option('linspector', 'plugins')
            self.__plugin_list = plugin_list.split(',')
            for plugin_option in self.__plugin_list:
                if plugin_option not in plugins:
                    log.info('loading plugin: ' + plugin_option)
                    plugin_package = 'linspector.plugins.' + plugin_option.lower()
                    plugin_module = importlib.import_module(plugin_package)
                    plugin = plugin_module.create(configuration, environment, log, self)
                    plugins[plugin_option.lower()] = plugin

        jobstores = {
            'memory': MemoryJobStore()
        }
        if configuration.get_option('linspector', 'max_threads') and not \
                configuration.get_option('linspector', 'scheduler_mode') == 'process':
            executors = {
                'default': ThreadPoolExecutor(int(configuration.get_option('linspector',
                                                                           'max_threads')))
            }
        else:
            executors = {
                'default': ThreadPoolExecutor(1024)
            }
        if configuration.get_option('linspector', 'scheduler_mode'):
            if configuration.get_option('linspector', 'scheduler_mode') == 'process':
                executors = {
                    'default': ProcessPoolExecutor(int(configuration.get_option('linspector',
                                                                                'max_processes')))
                }
        job_defaults = {
            # every scheduler job (monitor) must only exist once.
            'max_instances': 1
        }
        self.__scheduler['linspector'] = BackgroundScheduler(jobstores=jobstores,
                                                             executors=executors,
                                                             job_defaults=job_defaults)

        start_date = datetime.datetime.now()
        log.debug(monitors.get_monitors())
        monitors = self.__monitors.get_monitors()
        for monitor in monitors:
            log.debug(monitor)
            if configuration.get_option('linspector', 'delta_range'):
                time_delta = round(random.uniform(0.00, float(
                    configuration.get_option('linspector', 'delta_range'))), 3)
            else:
                time_delta = round(random.uniform(0.00, 60.000), 3)

            # TODO: write get functions in the monitor to get options. do not call
            #  get_monitor_configuration_option() here (example: get_start_date()).
            if monitors.get(monitor).get_monitor_configuration_option('args', 'start_date'):
                new_start_date = \
                    monitors.get(monitor).get_monitor_configuration_option('args', 'start_date')
            else:
                new_start_date = start_date + datetime.timedelta(seconds=time_delta)

            monitor_job = monitors.get(monitor)
            interval = monitor_job.get_interval()

            if configuration.get_option('linspector', 'timezone'):
                timezone = configuration.get_option('linspector', 'timezone')
                if monitors.get(monitor).get_monitor_configuration_option('args', 'timezone'):
                    timezone = monitors.get(monitor).get_monitor_configuration_option('args',
                                                                                      'timezone')
            else:
                timezone = 'UTC'

            # add cron and one time run jobs to Linspector. not only "interval" jobs should be
            # supported.
            scheduler_job = scheduler['linspector'].add_job(job_function, 'interval',
                                                            start_date=new_start_date,
                                                            seconds=interval, timezone=timezone,
                                                            args=[log, monitors.get(monitor)])

            monitor_job.set_job(scheduler_job)
            self.__jobs.append(monitor_job)
            log.info('scheduling job ' + monitor + ' with delta ' + str(time_delta) +
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
