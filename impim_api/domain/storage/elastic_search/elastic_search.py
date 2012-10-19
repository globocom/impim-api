#!/usr/bin/env python
# -*- coding: utf-8 -*-


from tornado import gen
from tornado.httpclient import AsyncHTTPClient
from tornado.httpclient import HTTPRequest

from impim_api.domain.storage.elastic_search import Parser
from impim_api.domain.storage.elastic_search import SearchRequestBody
from impim_api.domain.storage.elastic_search import Urls


class ElasticSearch(object):

    def __init__(self, config, http_client=AsyncHTTPClient()):
        self._http_client = http_client
        self._elastic_search_urls = Urls(config=config)
        self._elastic_search_parser = Parser()

    @gen.engine
    def search(self, callback, **search_arguments):
        elastic_search_request = self._build_elastic_search_request(**search_arguments)
        elastic_search_response = yield gen.Task(self._http_client.fetch, elastic_search_request)
        images_dict = self._elastic_search_parser.parse_images_from_search(elastic_search_response.body)
        callback(images_dict)

    def _build_elastic_search_request(self, **search_arguments):
        url = self._elastic_search_urls.search_url(Urls.IMAGE_TYPE)

        search_request_body = SearchRequestBody()
        search_request_body.from_index((search_arguments.get('page') - 1) * search_arguments.get('page_size'))
        search_request_body.size(search_arguments.get('page_size'))
        if search_arguments.get('q'):
            search_request_body.query_string(search_arguments.get('q'))
        if search_arguments.get('created_date_from'):
            search_request_body.range('createdDate').gte(search_arguments.get('created_date_from').isoformat())
        if search_arguments.get('created_date_to'):
            search_request_body.range('createdDate').lte(search_arguments.get('created_date_to').isoformat())
        if search_arguments.get('event_date_from'):
            search_request_body.range('eventDate').gte(search_arguments.get('event_date_from').isoformat())
        if search_arguments.get('event_date_to'):
            search_request_body.range('eventDate').lte(search_arguments.get('event_date_to').isoformat())
        search_request_body.sort([{'_score': 'desc'}, {'createdDate': {'order': 'desc', 'ignore_unmapped': True}}])

        return HTTPRequest(url, body=search_request_body.as_json(), allow_nonstandard_methods=True)
