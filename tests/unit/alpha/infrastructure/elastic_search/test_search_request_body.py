#!/usr/bin/env python
# -*- coding: utf-8 -*-


from json import loads
from unittest import TestCase

from images_api.alpha.infrastructure.elastic_search import SearchRequestBody


class SearchRequestBodyTestCase(TestCase):
    
    # es_req_body.from()
    # es_req_body.size()
    # es_req_body.query('blah')
    # es_req_body.range('createdDate').gte().lte()
    
    def setUp(self):
        super(SearchRequestBodyTestCase, self).setUp()
        self._request_body = SearchRequestBody()
    
    def test_from_index(self):
        self._request_body.from_index(1)
        assert loads(self._request_body.as_json()) == {'query': {'from': 1}}
    
    def test_size(self):
        self._request_body.size(1)
        assert loads(self._request_body.as_json()) == {'query': {'size': 1}}
    
    def test_query(self):
        self._request_body.query('my query')
        assert loads(self._request_body.as_json()) == {'query': {'query_string': {'query': 'my query'}}}
    
    def test_range(self):
        self._request_body.range('myField').gte(1).lte(10)
        assert loads(self._request_body.as_json()) == {'query': {'range': {'myField': {'gte': 1, 'lte': 10}}}}
    