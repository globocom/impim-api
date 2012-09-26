#!/usr/bin/env python
# -*- coding: utf-8 -*-

from tornado import gen
from tornado.httpclient import AsyncHTTPClient


class ImageResource(object):

    @gen.engine
    def all(self, callback):
        http_client = AsyncHTTPClient()
        response = yield gen.Task(http_client.fetch, 'http://localhost:9200/images-api/image/_search')
        callback(response.body)
