"""
This file is part of Linspector (https://linspector.org/)
Copyright (c) 2022 Johannes Findeisen <you@hanez.org>

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is furnished
to do so, subject to the following conditions:

The above copyright notice and this permission notice (including the next
paragraph) shall be included in all copies or substantial portions of the
Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS
FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS
OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY,
WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF
OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
"""

import calendar
import requests
import time

from logging import getLogger


from linspector.monitors.monitor import Monitor

logger = getLogger('linspector')


# TODO: check for all required configuration options and set defaults if needed.
class SpeedtestMonitor(Monitor):

    def __init__(self, configuration, environment):
        super().__init__(configuration, environment)
        self.__configuration = configuration
        self.__environment = environment

        self.__speedtest_maximum_speed = None
        self.__speedtest_average_speed = None
        self.__speedtest_time_elapsed = None

    def execute(self):
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
                logger.info('speedtest average: ' + str(self.__speedtest_average_speed) +
                            ', max: ' + str(self.__speedtest_maximum_speed) +
                            ', time: ' + str(self.__speedtest_time_elapsed))
            else:
                logger.warning('could not calculate download speed!')

            time.sleep(self.__configuration.get_speedtest_interval())

    def write_to_db(self):
        return
