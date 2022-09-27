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

from logging import getLogger

logger = getLogger('linspector')


class Linspector:

    def __init__(self, configuration, environment, monitors):
        self.__configuration = configuration
        self.__environment = environment
        self.__monitors = monitors

    # this function is just for testing purposes and can be removed some day
    def print_monitors_monitor_identifiers(self):
        # example on how to access the monitor objects in monitors
        monitors = self.__monitors.get_monitors()
        #print(monitors)
        for monitor in monitors:
            print(monitors.get(monitor).get_identifier())
