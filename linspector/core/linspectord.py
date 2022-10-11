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


# TODO: there is a bug when stopping the daemon. the pid_file is not being deleted. NEEDS A FIX!
class Linspectord:
    def __init__(self, configuration, environment, linspector, log):
        self.__configuration = configuration
        self.__environment = environment
        self.__linspector = linspector
        self.__log = log
        try:
            self.__pid_file = configuration.get_option('linspector', 'pid_file')
        except Exception as err:
            log.critical('daemonize error (no pid_file set): {0}'.str(format(err)))

    def daemonize(self):
        # daemonize the class using the UNIX double fork mechanism.

        # do first fork.
        try:
            pid = os.fork()
            if pid > 0:
                # exit first parent.
                sys.exit(0)
        except OSError as err:
            self.__log.critical('fork #1 failed: {0}'.str(format(err)))
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
            self.__log.critical('fork #2 failed: {0}'.str(format(err)))
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
        self.__log.info('starting daemon using pid_file: ' + str(self.__pid_file))
        try:
            with open(self.__pid_file, 'r') as pf:
                pid = int(pf.read().strip())
        except IOError:
            pid = None

        if pid:
            message = 'pid_file {0} already exist. daemon already running?'
            self.__log.critical(str(message.format(self.__pid_file)))
            sys.exit(1)

        # start the daemon.
        self.daemonize()
        self.run()

    def stop(self):
        # stop the daemon.
        self.__log.info('stopping daemon using pid_file: ' + str(self.__pid_file))
        # get the pid from the pid file.
        try:
            with open(self.__pid_file, 'r') as pf:
                pid = int(pf.read().strip())
        except IOError:
            pid = None

        if not pid:
            message = 'pid_file {0} does not exist. daemon not running?'
            self.__log.error(str(message.format(self.__pid_file)))
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
                self.__log.critical(str(err.args))
                sys.exit(1)

    def restart(self):
        # restart the daemon.
        self.__log.info('restarting daemon using pid_file: ' + str(self.__pid_file))
        self.stop()
        self.start()

    # maybe this function can be removed in the future because Linspector should rund endless when
    # starting scheduled jobs. need to cover this in the future. for now, it is useful for testing
    # while development because the daemon even runs when internally is nothing to do.
    @staticmethod
    def run():
        while True:
            pass
