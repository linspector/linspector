"""
This file is part of Linspector (https://linspector.org/)
Copyright (c) 2013-2023 Johannes Findeisen <you@hanez.org>. All Rights Reserved.
See LICENSE.
"""

import datetime
import importlib
import random
import time

from apscheduler.executors.pool import ThreadPoolExecutor, ProcessPoolExecutor
from apscheduler.jobstores.memory import MemoryJobStore
from apscheduler.schedulers.background import BackgroundScheduler
from pytz import utc


def job_execution(log, monitor):
    try:
        log.debug('executing job_function for monitor identifier: ' + monitor.get_identifier() +
                  ' with monitor object: ' + str(monitor))
        monitor.execute()
    except Exception as err:
        log.warning('execution failed for job_function for monitor identifier: ' +
                    monitor.get_identifier() + ' with monitor object: ' + str(monitor) +
                    ' error: ' + str(err))


class Linspector:
    def __init__(self, configuration, environment, log, monitors, plugins, scheduler):
        self._configuration = configuration
        self._environment = environment
        self._jobs = []
        self._log = log
        self._monitors = monitors
        self._plugin_list = []
        self._plugins = plugins
        self._scheduler = scheduler

        # load plugins
        log.info('message=loading plugins')
        if configuration.get_option('linspector', 'plugins'):
            plugin_list = configuration.get_option('linspector', 'plugins')
            self._plugin_list = plugin_list.split(',')
            for plugin_option in self._plugin_list:
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
                    'default': ThreadPoolExecutor(
                        int(configuration.get_option('linspector', 'max_threads'))),
                    'processpool': ProcessPoolExecutor(
                        int(configuration.get_option('linspector', 'max_processes')))
                }
        job_defaults = {
            'coalesce': True,
            # every scheduler job (monitor) must only exist once.
            'max_instances': 1
        }

        self._scheduler['linspector'] = BackgroundScheduler(jobstores=jobstores,
                                                            executors=executors,
                                                            job_defaults=job_defaults,
                                                            timezone=time.tzname[0])

        start_date = datetime.datetime.now()
        log.debug(monitors.get_monitors())
        monitors = self._monitors.get_monitors()
        for monitor in monitors:
            log.debug(monitor)
            if configuration.get_option('linspector', 'delta_range'):
                time_delta = round(random.uniform(0.00, float(
                    configuration.get_option('linspector', 'delta_range'))), 3)
            else:
                time_delta = round(random.uniform(0.00, 60.000), 3)

            if monitors.get(monitor).get_monitor_configuration_option('args', 'start_date'):
                new_start_date = \
                    monitors.get(monitor).get_monitor_configuration_option('args', 'start_date')
            else:
                new_start_date = start_date + datetime.timedelta(seconds=time_delta)

            monitor_job = monitors.get(monitor)
            interval = monitor_job.get_interval()

            if configuration.get_option('linspector', 'timezone'):
                timezone = configuration.get_option('linspector', 'timezone')
                if monitors.get(monitor).get_monitor_configuration_option('monitor', 'timezone'):
                    timezone = monitors.get(monitor).get_monitor_configuration_option('monitor',
                                                                                      'timezone')
            else:
                # set to local system timezone as default
                #timezone = datetime.datetime.now(datetime.timezone.utc).astimezone().tzname()
                timezone = time.tzname[0]

            # add cron and one time run jobs to Linspector. not only "interval" jobs should be
            # supported.
            scheduler_job = scheduler['linspector'].add_job(job_execution,
                                                            'interval',
                                                            start_date=new_start_date,
                                                            seconds=interval,
                                                            timezone=timezone,
                                                            id=monitor + '/' +
                                                            monitor_job.get_service() + '@' +
                                                            monitors.get(monitor).get_host(),
                                                            args=[log, monitors.get(monitor)])

            monitor_job.set_job(scheduler_job)
            self._jobs.append(monitor_job)
            log.info('identifier=' + monitor +
                     ' host=' + monitors.get(monitor).get_host() +
                     ' service=' + monitor_job.get_service() +
                     ' delta=' + str(time_delta) +
                     ' next=' + str(new_start_date) +
                     ' message=scheduling job')

        if configuration.get_option('linspector', 'start_scheduler') == 'true':
            self._scheduler['linspector'].start()
