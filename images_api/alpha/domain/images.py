#!/usr/bin/env python
# -*- coding: utf-8 -*-


from tornado import gen
from tornado.httpclient import AsyncHTTPClient
from tornado.httpclient import HTTPRequest

from images_api.alpha.domain import ElasticSearchParser
from images_api.alpha.infrastructure import ElasticSearchUrls
from images_api.alpha.infrastructure.elastic_search import SearchRequestBody


class Images(object):

    def __init__(self, config, http_client=AsyncHTTPClient()):
        self._http_client = http_client
        self._elastic_search_urls = ElasticSearchUrls(config=config)
        self._elastic_search_parser = ElasticSearchParser()

    @gen.engine
    def all(self, callback, **query_arguments):
        elastic_search_request = self._build_elastic_search_request(**query_arguments)
        elastic_search_response = yield gen.Task(self._http_client.fetch, elastic_search_request)
        
        images_dict = self._elastic_search_parser.parse_images_from_search(elastic_search_response.body)
        images_dict['pageSize'] = query_arguments.get('page_size')
        callback(images_dict)

    def _build_elastic_search_request(self, **query_arguments):
        url = self._elastic_search_urls.search_url(ElasticSearchUrls.IMAGE_TYPE)
        
        search_request_body = SearchRequestBody()
        search_request_body.from_index((query_arguments.get('page') - 1) * query_arguments.get('page_size'))
        search_request_body.size(query_arguments.get('page_size'))
        if query_arguments.get('q'):
            search_request_body.query_string(query_arguments.get('q'))
        if query_arguments.get('created_date_from'):
            search_request_body.range('createdDate').gte(query_arguments.get('created_date_from').isoformat())
        if query_arguments.get('created_date_to'):
            search_request_body.range('createdDate').lte(query_arguments.get('created_date_to').isoformat())
        
        return HTTPRequest(url, body=search_request_body.as_json(), allow_nonstandard_methods=True)
