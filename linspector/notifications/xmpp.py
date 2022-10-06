"""
This file is part of Linspector (https://linspector.org/)
Copyright (c) 2022 Johannes Findeisen <you@hanez.org>. All Rights Reserved.
See LICENSE (MIT license)
"""
import xmpp

from linspector.core.notification import Notification


def create(configuration, environment, log):
    return XMPPNotification(configuration, environment, log)


class XMPPNotification(Notification):
    def __init__(self, configuration, environment, log):
        super().__init__(configuration, environment, log)
        self.__configuration = configuration
        self.__environment = environment
        self.__log = log
