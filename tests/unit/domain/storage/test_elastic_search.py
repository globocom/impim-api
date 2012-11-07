#!/usr/bin/env python
# -*- coding: utf-8 -*-


from json import loads
from unittest import TestCase

import dateutil.parser

from impim_api.domain.storage.elastic_search import Parser
from impim_api.domain.storage.elastic_search import SearchRequestBody
from impim_api.domain.storage.elastic_search import Urls

from tests.support import MockConfig


class ParserTestCase(TestCase):

    def setUp(self):
        self._es_parser = Parser()

    def test_parse_images_from_search(self):
        es_json = """
            {
              "took" : 2,
              "timed_out" : false,
              "_shards" : {
                "total" : 5,
                "successful" : 5,
                "failed" : 0
              },
              "hits" : {
                "total" : 1,
                "max_score" : 1.0,
                "hits" : [ {
                  "_index" : "impim-api",
                  "_type" : "image",
                  "_id" : "Ngpkqld6T0SftZpL6KnMhA",
                  "_score" : 1.0,
                  "_source" : {
                    "credits": "Salve Jorge/TV Globo",
                    "url": "s.glbimg.com/et/nv/f/original/2012/09/24/istambul_asia.jpg",
                    "created_date": "2012-09-24T14:12:12",
                    "width": 940,
                    "event_date": "2012-09-24T14:12:12",
                    "title": "Istambul é a única cidade no mundo que fica em dois continentes: Europa e Ásia",
                    "height": 588
                  }
                } ]
              }
            }
        """

        parsed = self._es_parser.parse_images_from_search(es_json)

        assert parsed['total'] == 1
        assert len(parsed['items']) == 1
        assert parsed['items'][0]['credits'] == u"Salve Jorge/TV Globo"
        assert parsed['items'][0]['url'] == "s.glbimg.com/et/nv/f/original/2012/09/24/istambul_asia.jpg"
        assert parsed['items'][0]['created_date'] == dateutil.parser.parse("2012-09-24T14:12:12")
        assert parsed['items'][0]['width'] == 940
        assert parsed['items'][0]['event_date'] == dateutil.parser.parse("2012-09-24T14:12:12")
        assert parsed['items'][0]['title'] == u"Istambul é a única cidade no mundo que fica em dois continentes: Europa e Ásia"
        assert parsed['items'][0]['height'] == 588


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


class UrlsTestCase(TestCase):

    def setUp(self):
        super(UrlsTestCase, self).setUp()
        self._elastic_search_urls = Urls(config=MockConfig())

    def test_index_url(self):
        assert self._elastic_search_urls.index_url() == 'http://localhost:9200/impim-test'

    def test_type_url(self):
        assert self._elastic_search_urls.type_url(Urls.IMAGE_TYPE) == 'http://localhost:9200/impim-test/image'

    def test_search_url(self):
        assert self._elastic_search_urls.search_url(Urls.IMAGE_TYPE, q='search term') == 'http://localhost:9200/impim-test/image/_search?q=search+term'

    def test_refresh_url(self):
        assert self._elastic_search_urls.refresh_url() == 'http://localhost:9200/impim-test/_refresh'
