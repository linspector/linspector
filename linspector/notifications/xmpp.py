"""
This file is part of Linspector (https://linspector.org/)
Copyright (c) 2022 Johannes Findeisen <you@hanez.org>. All Rights Reserved.
See LICENSE (MIT license)
"""
import xmpp

from linspector.core.helpers import log
from linspector.core.notification import Notification


def create(configuration, environment):
    return XMPPNotification(configuration, environment)


class XMPPNotification(Notification):

    def __init__(self, configuration, environment):
        super().__init__(configuration, environment)
        self.__configuration = configuration
        self.__environment = environment
