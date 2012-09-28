#!/usr/bin/env python
# -*- coding: utf-8 -*-

from tornado import gen
from tornado.httpclient import AsyncHTTPClient

from images_api.alpha.domain import EsParser
from images_api.alpha.infrastructure import EsUrls

class Images(object):

    def __init__(self):
        self._http_client = AsyncHTTPClient()
        self._es_urls = EsUrls()
        self._es_parser = EsParser()

    @gen.engine
    def all(self, callback):
        response = yield gen.Task(self._http_client.fetch, self._es_urls.search_url(type=EsUrls.IMAGE_TYPE))
        json = self._es_parser.parse_images_from_search(response.body)
        callback(json)
