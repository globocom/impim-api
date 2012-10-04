#!/usr/bin/env python
# -*- coding: utf-8 -*-


from json import dumps

from tornado import gen
from tornado.httpclient import AsyncHTTPClient
from tornado.httpclient import HTTPRequest

from images_api.alpha.domain import ElasticSearchParser
from images_api.alpha.infrastructure import ElasticSearchUrls


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
        elastic_search_arguments = {
            'from': (query_arguments.get('page') - 1) * query_arguments.get('page_size'),
            'size': query_arguments.get('page_size'),
        }
        if query_arguments.get('q'):
            elastic_search_arguments['query'] = {'query_string': {'query': query_arguments.get('q')}}
        if query_arguments.get('created_date_from'):
            elastic_search_arguments['query'] = {
                'range': {
                    'createdDate': {
                        'gte': query_arguments.get('created_date_from').isoformat(),
                        'to': query_arguments.get('created_date_to').isoformat()
                    }
                }
            }
        return HTTPRequest(url, body=dumps(elastic_search_arguments), allow_nonstandard_methods=True)