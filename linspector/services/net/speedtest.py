"""
This file is part of Linspector (https://linspector.org/)
Copyright (c) 2022 Johannes Findeisen <you@hanez.org>. All Rights Reserved.
See LICENSE.txt (MIT license).
"""
import calendar
import time

import requests

from linspector.core.service import Service


def create(configuration, environment, log):
    return SpeedtestService(configuration, environment, log)


class SpeedtestService(Service):
    def __init__(self, configuration, environment, log):
        super().__init__(configuration, environment, log)
        self.__configuration = configuration
        self.__environment = environment
        self.__log = log

        self.__speedtest_maximum_speed = None
        self.__speedtest_average_speed = None
        self.__speedtest_time_elapsed = None

    def execute(self, **kwargs):
        while True:
            tmp_time = time.localtime(calendar.timegm(time.gmtime()))
            self.__environment.set_env_var('_speedtest_last_run_date',
                                           time.strftime('%Y-%m-%d %H:%M:%S',
                                                         tmp_time))

            self.__environment.set_env_var('_speedtest_last_run_timestamp',
                                           calendar.timegm(time.gmtime()))

            start = time.perf_counter()
            request = requests.get(self.__configuration.get_speedtest_url(), stream=True)
            size = int(request.headers.get('Content-Length'))
            downloaded = 0.0
            total_mbps = 0.0
            maximum_speed = 0.0
            total_chunks = 0.0

            if size is not None:
                for chunk in request.iter_content(1024 * 1024):
                    downloaded += len(chunk)
                    # megabytes per second
                    mbps = downloaded / (time.perf_counter() - start) / (1024 * 1024)
                    if mbps > maximum_speed:
                        maximum_speed = mbps
                    total_chunks += 1
                    total_mbps += mbps

                self.__speedtest_average_speed = total_mbps / total_chunks
                self.__environment.set_env_var('_speedtest_average_speed_megabyte_per_second',
                                               str(round(self.__speedtest_average_speed)))

                self.__speedtest_maximum_speed = maximum_speed
                self.__environment.set_env_var('_speedtest_maximum_speed_megabyte_per_second',
                                               str(round(self.__speedtest_maximum_speed)))

                self.__speedtest_time_elapsed = time.perf_counter() - start
                self.__environment.set_env_var('_speedtest_time_elapsed',
                                               str(self.__speedtest_time_elapsed))
                self.__log.info('speedtest average: ' + str(self.__speedtest_average_speed) +
                                ', max: ' + str(self.__speedtest_maximum_speed) +
                                ', time: ' + str(self.__speedtest_time_elapsed))
            else:
                self.__log.warning('could not calculate download speed!')

            time.sleep(self.__configuration.get_speedtest_interval())
