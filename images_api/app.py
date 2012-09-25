#!/usr/bin/env python
# -*- coding: utf-8 -*-

import tornado.web
from tornado import httpclient

from tornado_thumbor_url.handlers import GenerateThumborUrlHandler

from images_api.handlers import HealthCheckHandler
from images_api.alpha.handlers import SearchHandler


class JsonpEnabledThumborUrlHandler(GenerateThumborUrlHandler):

    def get(self, *args, **kwargs):
        callback_name = self.get_argument('callback', None)
        if not callback_name:
            callback_name = 'defaultCallback'
        self.write('%s("' % callback_name)
        super(JsonpEnabledThumborUrlHandler, self).get(*args, **kwargs)
        self.write('")')
        self.set_header('Content-Type', 'application/javascript')
        self.flush()


class ImagesApplication(tornado.web.Application):
    def __init__(self):
        httpclient.AsyncHTTPClient.configure(
                'tornado.curl_httpclient.CurlAsyncHTTPClient')
        handlers = [
            (r'/healthcheck(?:/|\.html)?', HealthCheckHandler),
            (r'/alpha/search/?', SearchHandler),
            (r'/thumbor_urls/?', JsonpEnabledThumborUrlHandler),
        ]
        super(ImagesApplication, self).__init__(handlers,
                thumbor_security_key='abc',
                thumbor_server_url='http://localhost:8888/')
