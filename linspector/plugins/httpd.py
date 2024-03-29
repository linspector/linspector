"""
This file is part of Linspector (https://linspector.org/)
Copyright (c) 2013-2023 Johannes Findeisen <you@hanez.org>. All Rights Reserved.
See LICENSE.
"""

import json

import cherrypy

from linspector.plugin import Plugin


def create(configuration, environment, linspector, log):
    return HTTPDPlugin(configuration, environment, linspector, log)


# TODO: check for all required configuration options and set defaults if needed.
class HTTPDPlugin(Plugin):

    def __init__(self, configuration, environment, linspector, log):
        super().__init__(configuration, environment, linspector, log)
        self._configuration = configuration
        self._environment = environment
        self._linspector = linspector

    @cherrypy.expose
    def index(self):
        return 'Hello world!'

    @cherrypy.expose
    def configuration(self):
        return '<!DOCTYPE html><html><head><title>[monipy-' + \
            self._environment.get_env_var("_version_") + '@' + \
            self._environment.get_env_var("_hostname") + '] configuration</title><meta ' + \
            'http-equiv="refresh" content="60"></head><body><pre ' + \
            'style="border:2px solid black;background:#1d2021;color:#f0751a;">' + \
            json.dumps(vars(self._configuration), sort_keys=True, indent=4) + \
            '</pre></body></html>'

    @cherrypy.expose
    def environment(self):
        return '<!DOCTYPE html><html><head><title>[monipy-' + \
            self._environment.get_env_var("_version_") + '@' + \
            self._environment.get_env_var("_hostname") + '] environment</title><meta ' + \
            'http-equiv="refresh" content="60"></head><body><pre ' + \
            'style="border:2px solid black;background:#1d2021;color:#f0751a;">' + \
            json.dumps(vars(self._environment), sort_keys=True, indent=4) + \
            '</pre></body></html>'

    @cherrypy.expose
    def playground(self):
        return 'My Playground!'

    def run(self):
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
        # cherrypy.config.update({
        #    'global': {
        #        'engine.autoreload.on': False
        #    }
        # })
        cherrypy.config.update({
            'global': {
                'server.socket_host': self._configuration.get_httpserver_host(),
                'server.socket_port': self._configuration.get_httpserver_port(),
                'environment': 'production'
            }
        })
        cherrypy.tree.mount(root=None, config=conf)
        cherrypy.quickstart(self, '/', conf)
        # cherrypy.server.bus.exit(self)
