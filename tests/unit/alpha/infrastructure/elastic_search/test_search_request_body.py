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
    
    def test_from_param(self):
        self._request_body.from_param(1)
        assert loads(self._request_body.as_json()) == {'query': {'from': 1}}
    