"""
This file is part of Linspector (https://linspector.org/)
Copyright (c) 2022-2023 Johannes Findeisen <you@hanez.org>. All Rights Reserved.
See LICENSE (MIT license).
"""
import pymysql.cursors

from linspector.database import Database


def create(configuration, environment, log):
    return MySQLDatabase(configuration, environment, log)


class MySQLDatabase(Database):

    def __init__(self, configuration, environment, log):
        super().__init__(configuration, environment, log)

        self._connection = None

        try:
            self._database = None
            if self._configuration.get_option('databases', 'mysql_database'):
                self._database = self._configuration.get_option('databases', 'mysql_database')

            self._host = None
            if self._configuration.get_option('databases', 'mysql_host'):
                self._host = self._configuration.get_option('databases', 'mysql_host')

            self._password = None
            if self._configuration.get_option('databases', 'mysql_password'):
                self._password = self._configuration.get_option('databases', 'mysql_password')

            self._user = None
            if self._configuration.get_option('databases', 'mysql_user'):
                self._user = self._configuration.get_option('databases', 'mysql_user')

            self._table = None
            if self._configuration.get_option('databases', 'mysql_table'):
                self._table = self._configuration.get_option('databases', 'mysql_table')

            self._user = None
            if self._configuration.get_option('databases', 'mysql_user'):
                self._user = self._configuration.get_option('databases', 'mysql_user')

        except Exception as err:
            log.warning('database configuration error: {0}'.format(err))

    def insert(self, host, identifier, json, message, service, status, timestamp):
        try:
            self._connection = pymysql.connect(cursorclass=pymysql.cursors.DictCursor,
                                               database=self._database,
                                               host=self._host,
                                               password=self._password,
                                               user=self._user)
            self._log.debug(self._connection)
        except Exception as err:
            self._log.warning('database connection failed: {0}'.format(err))

        try:
            with (self._connection):
                with self._connection.cursor() as cursor:
                    sql = 'INSERT INTO ' + self._table + ' (' \
                          'host, ' \
                          'identifier, ' \
                          'json, ' \
                          'message, ' \
                          'service, ' \
                          'status, ' \
                          'timestamp ' \
                          ') VALUES (\"' + \
                          str((host if host else "None")) + '\",\"' + \
                          str((identifier if identifier else "None")) + '\",\"' + \
                          str((json if json else "None")) + '\",\"' + \
                          str((message if message else "None")) + '\",\"' + \
                          str((service if service else "None")) + '\",\"' + \
                          str((status if status else "None")) + '\",\"' + \
                          str(timestamp) + '\")'
                    self._log.debug(sql)
                    cursor.execute(sql)
                self._connection.commit()
        except Exception as err:
            self._log.warning('database query failed: {0}'.format(err))
