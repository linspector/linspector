"""
This file is part of Linspector (https://linspector.org/)
Copyright (c) 2022-2023 Johannes Findeisen <you@hanez.org>. All Rights Reserved.
See LICENSE (MIT license).
"""
#from mysql.connector import connect, Error
import pymysql.cursors

from linspector.database import Database


def create(configuration, environment, log):
    return MySQLDatabase(configuration, environment, log)


class MySQLDatabase(Database):

    def __init__(self, configuration, environment, log):
        super().__init__(configuration, environment, log)

        try:
            self._connection = pymysql.connect(host='127.0.0.1',
                                               user='linspector',
                                               password='password',
                                               database='linspector',
                                               cursorclass=pymysql.cursors.DictCursor)
            log.debug(self._connection)
        except Exception as err:
            log.warning('database connection failed: {0}'.format(err))

        try:
            with self._connection.cursor() as cursor:
                sql = 'SELECT CURDATE()'
                cursor.execute(sql)
                result = cursor.fetchone()
                log.info(result)
        except Exception as err:
            log.warning('database query failed: {0}'.format(err))

    def insert(self):
        pass
