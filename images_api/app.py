#!/usr/bin/env python
# -*- coding: utf-8 -*-

import tornado.web
from tornado import httpclient

from tornado_thumbor_url.handlers import GenerateThumborUrlHandler

from images_api.handlers import HealthCheckHandler
from images_api.alpha.handlers import SearchHandler


class ImagesApplication(tornado.web.Application):
    def __init__(self):
        httpclient.AsyncHTTPClient.configure(
                'tornado.curl_httpclient.CurlAsyncHTTPClient')
        handlers = [
            (r'/healthcheck(?:/|\.html)?', HealthCheckHandler),
            (r'/alpha/search/?', SearchHandler),
            (r'/thumbor_urls/?', GenerateThumborUrlHandler),
        ]
        super(ImagesApplication, self).__init__(handlers,
                thumbor_security_key='abc',
                thumbor_server_url='http://localhost:8888/')
