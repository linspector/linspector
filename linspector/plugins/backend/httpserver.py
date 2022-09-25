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

import cherrypy
import json

from logging import getLogger
from linspector.plugins.plugin import Plugin

logger = getLogger('linspector')


# TODO: check for all required configuration options and set defaults if needed.
class HTTPServerPlugin(Plugin):

    def __init__(self, configuration, environment):
        super().__init__(configuration, environment)
        self.__configuration = configuration
        self.__environment = environment

    @cherrypy.expose
    def index(self):
        return 'Hello world!'

    @cherrypy.expose
    def configuration(self):
        return '<!DOCTYPE html><html><head><title>[monipy-' + \
               self.__environment.get_env_var("__version__") + '@' + \
               self.__environment.get_env_var("_hostname") + '] configuration</title><meta ' + \
               'http-equiv="refresh" content="60"></head><body><pre ' + \
               'style="border:2px solid black;background:#1d2021;color:#f0751a;">' + \
               json.dumps(vars(self.__configuration), sort_keys=True, indent=4) + \
               '</pre></body></html>'

    @cherrypy.expose
    def environment(self):
        return '<!DOCTYPE html><html><head><title>[monipy-' + \
               self.__environment.get_env_var("__version__") + '@' + \
               self.__environment.get_env_var("_hostname") + '] environment</title><meta ' + \
               'http-equiv="refresh" content="60"></head><body><pre ' + \
               'style="border:2px solid black;background:#1d2021;color:#f0751a;">' + \
               json.dumps(vars(self.__environment), sort_keys=True, indent=4) + \
               '</pre></body></html>'

    @cherrypy.expose
    def playground(self):
        return 'My Playground!'

    def run_server(self):
        conf = {
            '/': {
                #    'tools.sessions.on': True,
                #    'tools.staticdir.root': os.path.abspath(os.getcwd())
                'tools.response_headers.on': True,
                'tools.response_headers.headers': [('Content-Type', 'text/plain')],
            },
            '/configuration': {
                #    'request.dispatch': cherrypy.dispatch.MethodDispatcher(),
                'tools.response_headers.on': True,
                'tools.response_headers.headers': [('Content-Type', 'text/html')],
            },
            '/environment': {
                #    'request.dispatch': cherrypy.dispatch.MethodDispatcher(),
                'tools.response_headers.on': True,
                'tools.response_headers.headers': [('Content-Type', 'text/html')],
            },
            '/playground': {
                #    'tools.staticdir.on': True,
                #    'tools.staticdir.dir': './public'
            }
        }
        #cherrypy.config.update({
        #    'global': {
        #        'engine.autoreload.on': False
        #    }
        #})
        cherrypy.config.update({
            'global': {
                'server.socket_host': self.__configuration.get_httpserver_host(),
                'server.socket_port': self.__configuration.get_httpserver_port(),
                'environment': 'production'
            }
        })
        cherrypy.tree.mount(root=None, config=conf)
        cherrypy.quickstart(self, '/', conf)
        #cherrypy.server.bus.exit(self)
