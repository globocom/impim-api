#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import os
from os.path import expanduser, dirname

import tornado.web
from tornado import httpclient

from images_api.conf import Config
from images_api.handlers import HealthCheckHandler, JsonpEnabledThumborUrlHandler
from images_api.handlers import SearchHandler


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

        handlers = [
            (r'/healthcheck(?:/|\.html)?', HealthCheckHandler),
            (r'/alpha/search/?', SearchHandler),
            (r'/thumbor_urls/?', JsonpEnabledThumborUrlHandler),
        ]

        super(ImagesApplication, self).__init__(handlers,
                thumbor_security_key=self.config.THUMBOR_SECURITY_KEY,
                thumbor_server_url=self.config.THUMBOR_SERVER_URL,
                *args,
                **kwargs)
