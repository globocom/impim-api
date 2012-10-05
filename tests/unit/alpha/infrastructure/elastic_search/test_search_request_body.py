#!/usr/bin/env python
# -*- coding: utf-8 -*-


from json import loads
from unittest import TestCase

from images_api.alpha.infrastructure.elastic_search import SearchRequestBody


class SearchRequestBodyTestCase(TestCase):
    
    def setUp(self):
        super(SearchRequestBodyTestCase, self).setUp()
        self._request_body = SearchRequestBody()
    
    def test_from_index(self):
        self._request_body.from_index(1)
        assert loads(self._request_body.as_json()) == {'from': 1}
    
    def test_size(self):
        self._request_body.size(1)
        assert loads(self._request_body.as_json()) == {'size': 1}
    
    def test_query(self):
        self._request_body.query('my query')
        assert loads(self._request_body.as_json()) == {'query': {'query_string': {'query': 'my query'}}}
    
    def test_range(self):
        self._request_body.range('myField').gte(1).lte(10)
        assert loads(self._request_body.as_json()) == {'query': {'range': {'myField': {'gte': 1, 'lte': 10}}}}
    
    def test_range_twice(self):
        self._request_body.range('myField').gte(1)
        self._request_body.range('myField').lte(10)
        assert loads(self._request_body.as_json()) == {'query': {'range': {'myField': {'gte': 1, 'lte': 10}}}}
    
    def test_range_twice_different_arguments(self):
        self._request_body.range('myField1').gte(1)
        self._request_body.range('myField2').lte(10)
        assert loads(self._request_body.as_json()) == {'query': {'range': {'myField1': {'gte': 1}, 'myField2': {'lte': 10}}}}
