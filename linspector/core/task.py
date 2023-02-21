"""
This file is part of Linspector (https://linspector.org/)
Copyright (c) 2022 Johannes Findeisen <you@hanez.org>. All Rights Reserved.
See LICENSE.txt (MIT license).
"""
from queue import Queue
from threading import Thread

from linspector.core.singleton import Singleton

KEY_TYPE = "type"
KEY_ARGS = "args"
KEY_CLASS = "class"


class Task:
    def __init__(self, configuration, environment, log, **kwargs):
        self.__args = {}
        self.__configuration = configuration
        self.__environment = environment
        self.__log = log

        if KEY_ARGS in kwargs:
            self.add_arguments(kwargs[KEY_ARGS])
        elif self.needs_arguments():
            raise Exception("Error: needs arguments but none provided!")

        if KEY_CLASS in kwargs:
            self.name = kwargs[KEY_CLASS]
        else:
            self.name = self.__class__

        self._type = None
        if KEY_TYPE in kwargs:
            self._type = kwargs[KEY_TYPE]

    def get_task_type(self):
        return str(self._type)

    def get_config_name(self):
        return str(self.name)

    def add_arguments(self, args):
        for key, val in args.items():
            self.__args[key] = val

    def get_arguments(self):
        return self.__args

    # def set_member(self, member):
    #    self.member = member

    def needs_arguments(self):
        return False

    def execute(self, job):
        try:
            self.execute(job)
        except Exception as e:
            # logger.debug("Task execute failed!!!")
            raise e


# i believe the singleton pattern is not required here because all tasks are stored as singleton in
# a dict already, and they can be executed directly in the equivalent monitor. need to discover this
# when tasks are being implemented. this is from the old version of Linspector...
# UPDATE: i see that task runners should be executed as separate threads, so maybe they should be
# singleton here to not instantiate more than one instance inside each task. don't know actually...
@Singleton
class TaskRunner:
    def __init__(self, configuration, environment, log):
        self.__configuration = configuration
        self.__environment = environment
        self.__log = log
        self.queue = Queue()
        self.task_infos = []
        task_thread = Thread(target=self._run_worker_thread)
        self._instant_end = False
        self._running = True
        task_thread.daemon = True
        task_thread.start()

    def _run_worker_thread(self):
        while self.is_running() or not self.is_instant_end():

            try:
                msg, task = self.queue.get()
                if task:
                    self.__log.debug('starting task execution...')
                    # task.execute(msg)
                self.queue.task_done()

            except Exception as err:
                self.__log.error('error ' + str(err))

    def is_instant_end(self):
        return self._instant_end

    def is_running(self):
        return self._running

    def stop(self):
        self._running = False

    def stop_immediately(self):
        self._running = False
        self._instant_end = True

    def schedule_task(self, msg, task):
        self.queue.put((msg, task))
