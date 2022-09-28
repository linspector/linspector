"""
This file is part of Linspector (https://linspector.org/)
Copyright (c) 2022 Johannes Findeisen <you@hanez.org>. All Rights Reserved.
See LICENSE (MIT license)
"""
import atexit
import os
import signal
import sys
import time

from logging import getLogger

logger = getLogger('linspector')


class Linspectord:
    def __init__(self, pid_file, configuration, environment, linspector):
        self.__pid_file = pid_file
        self.__configuration = configuration
        self.__environment = environment
        self.__linspector = linspector

    def daemonize(self):
        # daemonize the class using the UNIX double fork mechanism.

        # do first fork.
        try:
            pid = os.fork()
            if pid > 0:
                # exit first parent.
                sys.exit(0)
        except OSError as err:
            logger.error(str('fork #1 failed: {0}'.format(err)))
            sys.exit(1)

        # decouple from parent environment.
        os.chdir('/')
        os.setsid()
        os.umask(0)

        # do second fork.
        try:
            pid = os.fork()
            if pid > 0:
                # Exit from second parent.
                sys.exit(0)
        except OSError as err:
            logger.error(str('fork #2 failed: {0}'.format(err)))
            sys.exit(1)

        # redirect standard file descriptors.
        sys.stdout.flush()
        sys.stderr.flush()
        si = open(os.devnull, 'r')
        so = open(os.devnull, 'a+')
        se = open(os.devnull, 'a+')

        os.dup2(si.fileno(), sys.stdin.fileno())
        os.dup2(so.fileno(), sys.stdout.fileno())
        os.dup2(se.fileno(), sys.stderr.fileno())

        # write pid file.
        atexit.register(self.delete_pid)

        pid = str(os.getpid())
        with open(self.__pid_file, 'w+') as f:
            f.write(pid + '\n')

    def delete_pid(self):
        os.remove(self.__pid_file)

    def start(self):
        # start the daemon. check for a pidfile to see if the daemon already runs before.

        try:
            with open(self.__pid_file, 'r') as pf:
                pid = int(pf.read().strip())
        except IOError:
            pid = None

        if pid:
            message = 'pid_file {0} already exist. daemon already running?'
            logger.error(str(message.format(self.__pid_file)))
            sys.exit(1)

        # start the daemon.
        self.daemonize()
        self.run()

    def stop(self):
        # stop the daemon.

        # get the pid from the pid file.
        try:
            with open(self.__pid_file, 'r') as pf:
                pid = int(pf.read().strip())
        except IOError:
            pid = None

        if not pid:
            message = 'pid_file {0} does not exist. daemon not running?'
            logger.error(str(message.format(self.__pid_file)))
            return  # not an error in a restart

        # try killing the daemon process.
        try:
            while 1:
                os.kill(pid, signal.SIGTERM)
                time.sleep(0.1)
        except OSError as err:
            e = str(err.args)
            if e.find('no such process') > 0:
                if os.path.exists(self.__pid_file):
                    os.remove(self.__pid_file)
            else:
                logger.error(str(err.args))
                sys.exit(1)

    def restart(self):
        # restart the daemon.

        self.stop()
        self.start()

    def run(self):
        """
        a good place to execute stuff after the process has been daemonized by start() or restart().
        """
