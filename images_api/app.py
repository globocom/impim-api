#!/usr/bin/env python
# -*- coding: utf-8 -*-

import tornado.web
from tornado import httpclient

from tornado_thumbor_url.handlers import GenerateThumborUrlHandler

from images_api.handlers import HealthCheckHandler
from images_api.alpha.handlers import SearchHandler


class JsonpEnabledThumborUrlHandler(GenerateThumborUrlHandler):

    def flush(self, *args, **kwargs):
        self._original_flush = super(JsonpEnabledThumborUrlHandler, self).flush

    def get(self, *args, **kwargs):
        callback_name = self.get_argument('callback', None)
        if not callback_name:
            callback_name = 'defaultCallback'
        self.write('%s("' % callback_name)
        super(JsonpEnabledThumborUrlHandler, self).get(*args, **kwargs)
        self.write('")')
        self.clear_header('Content-Type')
        self.set_header('Content-Type', 'application/javascript')
        self._original_flush()
        self.flush = self._original_flush


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
