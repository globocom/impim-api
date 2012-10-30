#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import os
from os.path import expanduser, dirname

import tornado.web
from tornado import httpclient
from tapioca import TornadoRESTful

from impim_api.conf import Config
from impim_api.handlers import HealthCheckHandler, JsonpEnabledThumborUrlHandler
from impim_api.handlers import ImagesResourceHandler


class ImagesApplication(tornado.web.Application):

    def __init__(self, conf_file=None, base_url=None, *args, **kwargs):
        here = dirname(dirname(sys.argv[0]))
        self.config = Config.load(path=conf_file, conf_name="impim_api.conf",
            lookup_paths=[
                here,
                os.curdir,
                expanduser('~'),
                '/etc/',
                dirname(__file__),
            ])

        rest_api = TornadoRESTful(version='alpha', base_url=base_url,
                discovery=True)
        rest_api.add_resource('alpha/images', ImagesResourceHandler)

        handlers = [
            (r'/healthcheck(?:/|\.html)?', HealthCheckHandler),
            (r'/thumbor_urls/?', JsonpEnabledThumborUrlHandler),
        ] + rest_api.get_url_mapping()

        super(ImagesApplication, self).__init__(handlers,
                thumbor_security_key=self.config.THUMBOR_SECURITY_KEY,
                thumbor_server_url=self.config.THUMBOR_SERVER_URL,
                *args,
                **kwargs)
