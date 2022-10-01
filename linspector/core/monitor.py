"""
This file is part of Linspector (https://linspector.org/)
Copyright (c) 2022 Johannes Findeisen <you@hanez.org>. All Rights Reserved.
See LICENSE (MIT license)
"""
import configparser
import hashlib
import importlib

from datetime import datetime
from binascii import crc32

from linspector.core.helpers import log
from linspector.core.task import Task, TaskExecutor


class Monitor:

    def __init__(self, configuration, environment, identifier, monitor_configuration, notifications,
                 services, tasks, kwargs):
        self.__args = kwargs
        self.__configuration = configuration
        self.__environment = environment
        self.__identifier = identifier
        self.__interval = int(monitor_configuration.get('monitor', 'interval'))
        self.__monitor_configuration = monitor_configuration
        self.__notification_list = []
        self.__notifications = notifications
        self.__service = monitor_configuration.get('monitor', 'service')
        self.__services = services
        self.__task_list = []  # put tasks for the dedicated job here.
        self.__tasks = tasks

        self.service = self.__service
        self.host = monitor_configuration.get('monitor', 'hosts')

        try:
            self.hostgroups = monitor_configuration.get('monitor', 'hostgroups')
        except configparser.NoOptionError as err:
            self.hostgroups = "None"

        self.job_threshold = 0
        self.enabled = True
        self.scheduler_job = None
        # the job_id is a sha256 string.
        self.job_id = self.generate_job_id()

        """
        NONE     job was not executed
        OK       when everything is fine
        WARNING  when a job has errors but not the threshold overridden
        RECOVER  when a job recovers e.g. the threshold decrements (not implemented)
        ERROR    when a jobs threshold is overridden
        UNKNOWN  when a job throws an exception which is not handled by the job itself (not 
        implemented)
        """
        self.status = "NONE"
        self.last_execution = None
        #self.monitor_information = MonitorInformation(self.job_id, self.hostgroup, self.host,
        #                                              self.service)
        self.monitor_information = MonitorInformation(self.job_id, self.service)

        try:
            if configuration.get_option('linspector', 'notifications') or \
                    monitor_configuration.get('monitor', 'notifications'):

                if configuration.get_option('linspector', 'notifications') and \
                        monitor_configuration.get('monitor', 'notifications'):

                    notification_list = \
                        configuration.get_option('linspector', 'notifications') + ',' + \
                        monitor_configuration.get('monitor', 'notifications')
                elif configuration.get_option('linspector', 'notifications'):
                    notification_list = configuration.get_option('linspector', 'notifications')
                elif monitor_configuration.get('monitor', 'notifications'):
                    notification_list = monitor_configuration.get('monitor', 'notifications')
                else:
                    notification_list = None

                self.__notification_list = notification_list.split(',')

            for notification_option in notification_list.split(','):
                if notification_option not in notifications:
                    notification_package = 'linspector.notifications.' + notification_option.lower()
                    notification_module = importlib.import_module(notification_package)
                    notification = notification_module.create(configuration, environment)
                    notifications[notification_option.lower()] = notification
        except configparser.NoOptionError as err:
            self.__notifications = notifications

        if self.__monitor_configuration.get('monitor', 'service'):
            if monitor_configuration.get('monitor', 'service') not in services:
                service_package = 'linspector.services.' + \
                                  monitor_configuration.get('monitor', 'service').lower()

                service_module = importlib.import_module(service_package)
                self.__service = monitor_configuration.get('monitor', 'service').lower()
                service = service_module.create(configuration, environment)
                self.__services[monitor_configuration.get('monitor', 'service').lower()] = service
        try:
            if configuration.get_option('linspector', 'tasks') or \
                    monitor_configuration.get('args', 'tasks'):

                if configuration.get_option('linspector', 'tasks') and \
                        monitor_configuration.get('args', 'tasks'):

                    task_list = configuration.get_option('linspector', 'tasks') + ',' + \
                                monitor_configuration.get('args', 'tasks')
                elif configuration.get_option('linspector', 'tasks'):
                    task_list = configuration.get_option('linspector', 'tasks')
                elif monitor_configuration.get('args', 'tasks'):
                    task_list = monitor_configuration.get('args', 'tasks')
                else:
                    task_list = None

                self.__task_list = task_list.split(',')

                for task_option in task_list.split(','):
                    if task_option not in tasks:
                        task_package = 'linspector.tasks.' + task_option.lower()
                        task_module = importlib.import_module(task_package)
                        task = task_module.create(configuration, environment)
                        tasks[task_option.lower()] = task
        except configparser.NoOptionError:
            self.__tasks = tasks

    def get_identifier(self):
        return self.__identifier

    def get_interval(self):
        return self.__interval

    def get_monitor_configuration(self):
        return self.__monitor_configuration

    def get_monitor_configuration_option(self, section, option):
        if self.__monitor_configuration.has_option(section, option):
            return self.__monitor_configuration.get(section, option)
        else:
            return None
        return self.__monitor_configuration

    def get_service(self):
        return self.__service

    def __str__(self):
        return str(self.__dict__)

    def hex_string(self):
        ret = hex(crc32(bytes(self.host + self.hostgroups + self.service, 'utf-8')))
        #ret = self.__hex__()
        if ret[0] == "-":
            ret = ret[3:]
        else:
            ret = ret[2:]
        while len(ret) < 8:
            ret = "0" + ret
        return ret

    def generate_job_id(self):
        return hashlib.sha256(bytes(self.__identifier + self.host + self.hostgroups + self.service,
                                    'utf-8')).hexdigest()

    def set_job(self, scheduler_job):
        self.scheduler_job = scheduler_job

    def set_enabled(self, enabled=True):
        self.enabled = enabled

    def handle_threshold(self, service_threshold, execution_successful):
        if execution_successful:
            if self.job_threshold > 0:
                if "threshold_reset" in self.core and self.core["threshold_reset"]:
                    #logger.info("Job " + self.get_job_id() + ", Threshold Reset")
                    self.job_threshold = 0
                else:
                    #logger.info("Job " + self.get_job_id() + ", Threshold Decrement")
                    self.job_threshold -= 1

            self.status = "OK"
            self.monitor_information.set_status(self.status)
            self.monitor_information.inc_job_overall_wins()
        else:
            self.status = "WARNING"
            self.monitor_information.set_status(self.status)
            self.monitor_information.inc_job_overall_fails()
            self.job_threshold += 1

        if self.job_threshold >= service_threshold:
            #logger.info("Job " + self.get_job_id() + ", Threshold reached!")
            self.status = "ERROR"
            self.monitor_information.set_status(self.status)

    def handle_tasks(self, monitor_information):
        for task in self.__tasks:
            if self.status.lower() in task.get_task_type().lower():
                log('debug', 'executing task of type: ' + self.status)
                # tasks can but should not be executed here. putting them in a queue is the better
                # solution to execute them in a serial process.
                #TaskExecutor.instance().schedule_task(monitor_information, task)

    def handle_call(self):
        log('info', 'handle call to monitor with identifier: ' + self.__identifier)
        #logger.debug("handle call")
        #logger.debug(self.service)
        if self.enabled:
            self.last_execution = None
            try:
                self.last_execution = MonitorExecution(self.get_host())
                #self.__services[self.__service].execute(self.last_execution)
                self.__services[self.__service].execute(**self.__args)
            except Exception as err:
                log('error', err)

            #self.last_execution.set_execution_end()

            #self.handle_threshold(self.service.get_threshold(),
            #                      self.last_execution.was_successful())

            #log.info("Job " + self.get_job_id() +
            #            ", Code: " + str(self.last_execution.get_error_code()) +
            #            ", Message: " + str(self.last_execution.get_message()))

            #self.monitor_information.set_response_message(
            #    self.last_execution.get_response_message(self))

            #self.handle_tasks(self.monitor_information)
        else:
            log('info', "job " + self.get_job_id() + " disabled")

    def get_host(self):
        return self.host

    def get_hostgroups(self):
        return self.hostgroups


class MonitorExecution:
    def __init__(self, host):
        self.execution_start = datetime.now()
        self.execution_end = -1
        self.host = host
        self.error_code = -1
        self.message = None
        self.kwargs = None

    def get_host_name(self):
        return self.host

    def get_message(self):
        return self.message

    def get_kwargs(self):
        return self.kwargs

    def set_execution_end(self):
        self.execution_end = datetime.now()

    def get_error_code(self):
        return self.error_code

    def was_successful(self):
        return self.get_error_code() == 0

    def set_result(self, error_code=0, message="", kwargs=None):
        self.error_code = error_code
        self.message = message
        self.kwargs = kwargs

    def get_response_message(self, job):
        msg = str(job.status) + " [" + job.service.get_config_name() + ": " + str(job.get_job_id()) + "] " + \
              str(job.get_hostgroup()) + " " + str(job.get_host())
        if self.get_message() is not None:
            msg += " " + str(self.get_message())
        if self.get_kwargs() is not None:
            msg += " " + str(self.get_kwargs())
        return msg


class MonitorInformation:
    def __init__(self, job_id, service):
        self.job_id = job_id
        #self.hostgroup = hostgroup
        #self.host = host
        self.service = service

        self.response_massage = None
        self.period = None
        self.next_run = None
        self.runs = 0
        self.enabled = None
        self.threshold = 0
        self.fails = 0
        self.job_overall_fails = 0
        self.job_overall_wins = 0
        self.last_execution = None
        self.last_run = None
        self.last_fail = None
        self.last_success = None
        self.last_disabled = None
        self.last_enabled = None
        self.last_threshold_override = None
        self.last_escalation = None
        self.status = "NONE"

    def inc_job_overall_fails(self):
        self.job_overall_fails += 1

    def inc_job_overall_wins(self):
        self.job_overall_wins += 1

    def get_job_id(self):
        return self.job_id

    def get_response_message(self):
        return self.response_massage

    def set_response_message(self, msg):
        self.response_massage = msg

    def get_status(self):
        return self.status

    def set_status(self, status):
        self.status = status
