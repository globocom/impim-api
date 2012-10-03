#!/usr/bin/env python
# -*- coding: utf-8 -*-

from tornado import gen
from tornado.httpclient import AsyncHTTPClient

from images_api.alpha.domain import ElasticSearchParser
from images_api.alpha.infrastructure import ElasticSearchUrls

class Images(object):

    def __init__(self, config, http_client=AsyncHTTPClient()):
        self._http_client = http_client
        self._elastic_search_urls = ElasticSearchUrls(config=config)
        self._elastic_search_parser = ElasticSearchParser()

    @gen.engine
    def all(self, callback, page=1, page_size=10):
        page = int(page)
        page_size = int(page_size)
        es_args = {
            'from': (page - 1) * page_size,
            'size': page_size,
        }
        
        url = self._elastic_search_urls.search_url(ElasticSearchUrls.IMAGE_TYPE, **es_args)
        elastic_search_response = yield gen.Task(self._http_client.fetch, url)
        
        images_dict = self._elastic_search_parser.parse_images_from_search(elastic_search_response.body)
        images_dict['pageSize'] = page_size
        callback(images_dict)
