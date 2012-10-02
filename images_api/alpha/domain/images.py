#!/usr/bin/env python
# -*- coding: utf-8 -*-

from tornado import gen
from tornado.httpclient import AsyncHTTPClient

from images_api.alpha.domain import EsParser
from images_api.alpha.infrastructure import EsUrls

class Images(object):

    def __init__(self, config, http_client=AsyncHTTPClient()):
        self._http_client = http_client
        self._es_urls = EsUrls(config=config)
        self._es_parser = EsParser()

    @gen.engine
    def all(self, callback, page=1, page_size=10):
        es_args = {
            'from': (page - 1) * page_size,
            'size': page_size,
        }
        
        response = yield gen.Task(self._http_client.fetch, self._es_urls.search_url(type=EsUrls.IMAGE_TYPE, **es_args))
        json = self._es_parser.parse_images_from_search(response.body)
        callback(json)
