"""
This file is part of Linspector (https://linspector.org/)
Copyright (c) 2013-2023 Johannes Findeisen <you@hanez.org>. All Rights Reserved.
See LICENSE.
"""

import calendar
import time

import requests

from linspector.service import Service


def create(configuration, environment, log):
    return SpeedtestService(configuration, environment, log)


class SpeedtestService(Service):
    def __init__(self, configuration, environment, log):
        super().__init__(configuration, environment, log)
        self._configuration = configuration
        self._environment = environment
        self._log = log

        self._speedtest_maximum_speed = None
        self._speedtest_average_speed = None
        self._speedtest_time_elapsed = None

    def execute(self, **kwargs):
        while True:
            tmp_time = time.localtime(calendar.timegm(time.gmtime()))
            self._environment.set_env_var('_speedtest_last_run_date',
                                          time.strftime('%Y-%m-%d %H:%M:%S',
                                                        tmp_time))

            self._environment.set_env_var('_speedtest_last_run_timestamp',
                                          calendar.timegm(time.gmtime()))

            start = time.perf_counter()
            request = requests.get(self._configuration.get_speedtest_url(), stream=True)
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

                self._speedtest_average_speed = total_mbps / total_chunks
                self._environment.set_env_var('_speedtest_average_speed_megabyte_per_second',
                                              str(round(self._speedtest_average_speed)))

                self._speedtest_maximum_speed = maximum_speed
                self._environment.set_env_var('_speedtest_maximum_speed_megabyte_per_second',
                                              str(round(self._speedtest_maximum_speed)))

                self._speedtest_time_elapsed = time.perf_counter() - start
                self._environment.set_env_var('_speedtest_time_elapsed',
                                              str(self._speedtest_time_elapsed))
                self._log.info('speedtest average: ' + str(self._speedtest_average_speed) +
                               ', max: ' + str(self._speedtest_maximum_speed) +
                               ', time: ' + str(self._speedtest_time_elapsed))
            else:
                self._log.warning('could not calculate download speed!')

            time.sleep(self._configuration.get_speedtest_interval())
