"""
This file is part of Linspector (https://linspector.org/)
Copyright (c) 2013-2023 Johannes Findeisen <you@hanez.org>. All Rights Reserved.
See LICENSE.
"""

import pymysql.cursors

from linspector.task import Task


def create(configuration, environment, log):
    return MySQLTask(configuration, environment, log)


class MySQLTask(Task):

    def __init__(self, configuration, environment, log):
        super().__init__(configuration, environment, log)

        self._connection = None

        try:
            self._database = None
            if self._configuration.get_option('tasks', 'mysql_database'):
                self._database = self._configuration.get_option('tasks', 'mysql_database')

            self._host = None
            if self._configuration.get_option('tasks', 'mysql_host'):
                self._host = self._configuration.get_option('tasks', 'mysql_host')

            self._password = None
            if self._configuration.get_option('tasks', 'mysql_password'):
                self._password = self._configuration.get_option('tasks', 'mysql_password')

            self._user = None
            if self._configuration.get_option('tasks', 'mysql_user'):
                self._user = self._configuration.get_option('tasks', 'mysql_user')

            self._table = None
            if self._configuration.get_option('tasks', 'mysql_table'):
                self._table = self._configuration.get_option('tasks', 'mysql_table')

            self._user = None
            if self._configuration.get_option('tasks', 'mysql_user'):
                self._user = self._configuration.get_option('tasks', 'mysql_user')

        except Exception as err:
            log.error('task mysql configuration error: {0}'.format(err))

    def execute(self, error_count, host, identifier, json, log, service, status, timestamp):
        try:
            self._connection = pymysql.connect(cursorclass=pymysql.cursors.DictCursor,
                                               database=self._database,
                                               host=self._host,
                                               password=self._password,
                                               user=self._user)
            self._log.debug(self._connection)
        except Exception as err:
            self._log.error('task mysql connection failed: {0}'.format(err))

        try:
            with (self._connection):
                with self._connection.cursor() as cursor:
                    sql = 'INSERT INTO ' + self._table + ' (' \
                          'error_count, ' \
                          'host, ' \
                          'identifier, ' \
                          'json, ' \
                          'log, ' \
                          'service, ' \
                          'status, ' \
                          'timestamp ' \
                          ') VALUES (\"' + \
                          str((error_count if error_count else '0')) + '\",\"' + \
                          str((host if host else 'None')) + '\",\"' + \
                          str((identifier if identifier else 'None')) + '\",\"' + \
                          str((json if json else 'None')) + '\",\"' + \
                          str((log if log else 'None')) + '\",\"' + \
                          str((service if service else 'None')) + '\",\"' + \
                          str((status if status else 'UNKNOWN')) + '\",\"' + \
                          str(timestamp) + '\")'
                    self._log.debug(sql)
                    cursor.execute(sql)
                self._connection.commit()
        except Exception as err:
            self._log.error('task mysql query failed: {0}'.format(err))
