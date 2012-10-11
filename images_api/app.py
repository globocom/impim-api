#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import os
from os.path import expanduser, dirname

import tornado.web
from tornado import httpclient

from images_api.conf import Config
from images_api.rest_api import TornadoRESTful
from images_api.handlers import HealthCheckHandler, JsonpEnabledThumborUrlHandler
from images_api.handlers import ImagesResourceHandler


class ImagesApplication(tornado.web.Application):

    def __init__(self, conf_file=None, *args, **kwargs):
        here = dirname(dirname(sys.argv[0]))
        self.config = Config.load(path=conf_file, conf_name="images_api.conf",
            lookup_paths=[
                here,
                os.curdir,
                expanduser('~'),
                '/etc/'
            ])

        rest_api = TornadoRESTful()
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
