#!/usr/bin/env python
# -*- coding: utf-8 -*-

from tornado import gen
from tornado.httpclient import AsyncHTTPClient

from images_api.alpha.domain import EsParser

class ImageResource(object):

    def __init__(self):
        self._es_parser = EsParser()

    @gen.engine
    def all(self, callback):
        http_client = AsyncHTTPClient()
        response = yield gen.Task(http_client.fetch, 'http://localhost:9200/images-api/image/_search')
        json = self._es_parser.parse_images_from_search(response.body)
        callback(json)
