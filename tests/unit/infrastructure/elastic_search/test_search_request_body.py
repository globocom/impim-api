#!/usr/bin/env python
# -*- coding: utf-8 -*-


from json import loads
from unittest import TestCase

from impim_api.infrastructure.elastic_search import SearchRequestBody


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
    
    def test_query_string(self):
        self._request_body.query_string('my query')
        assert loads(self._request_body.as_json()) == {u'query': {u'bool': {u'must': [{u'query_string': {u'query': u'my query'}}]}}}
    
    def test_range(self):
        self._request_body.range('myField').gte(1).lte(10)
        assert loads(self._request_body.as_json()) == {u'query': {u'bool': {u'must': [{u'range': {u'myField': {u'gte': 1, u'lte': 10}}}]}}}
    
    def test_range_twice(self):
        self._request_body.range('myField').gte(1)
        self._request_body.range('myField').lte(10)
        assert loads(self._request_body.as_json()) == {u'query': {u'bool': {u'must': [{u'range': {u'myField': {u'gte': 1, u'lte': 10}}}]}}}
    
    def test_range_twice_different_arguments(self):
        self._request_body.range('myField1').gte(1)
        self._request_body.range('myField2').lte(10)
        assert loads(self._request_body.as_json()) == {u'query': {u'bool': {u'must': [{u'range': {u'myField1': {u'gte': 1}}}, {u'range': {u'myField2': {u'lte': 10}}}]}}}
    
    def test_query_string_and_range(self):
        self._request_body.query_string('my query')
        self._request_body.range('myField').gte(1).lte(10)
        assert loads(self._request_body.as_json()) == {
            u'query': {
                u'bool': {
                    u'must': [{
                        u'query_string': {u'query': u'my query'}},
                        {u'range': {u'myField': {u'gte': 1, u'lte': 10}}
                    }]
                }
            }
        }
        
    def test_sort(self):
        self._request_body.sort([{'_score': 'desc'}, {'createdDate': 'desc'}])
        assert loads(self._request_body.as_json()) == {'sort': [{'_score': 'desc'}, {'createdDate': 'desc'}]}
