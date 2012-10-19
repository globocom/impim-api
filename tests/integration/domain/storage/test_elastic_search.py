#!/usr/bin/env python
# -*- coding: utf-8 -*-

from datetime import datetime
from json import dumps, loads

from tornado.httpclient import AsyncHTTPClient
from tornado.testing import AsyncTestCase

from impim_api.domain.storage import ElasticSearch
from impim_api.domain.storage.elastic_search import Urls

from tests.support import AsyncHTTPClientMixin
from tests.support import ElasticSearchMixin
from tests.support import es_cleanup
from tests.support import MockConfig


class ElasticSearchTestCase(AsyncTestCase, AsyncHTTPClientMixin, ElasticSearchMixin):

    def setUp(self):
        super(ElasticSearchTestCase, self).setUp()

        self.http_client = AsyncHTTPClient(self.io_loop)
        config = MockConfig()
        self._elastic_search_urls = Urls(config)
        self._elastic_search = ElasticSearch(config=config, http_client=self.http_client)

        es_cleanup(self._elastic_search_urls)

    def test_search(self):
        self.post_to_elastic_search(self._elastic_search_urls.type_url(Urls.IMAGE_TYPE), {
            'title': u'Title', 'createdDate': '2012-10-04T13:00:00'
        })

        self._elastic_search.search(self.assert_search_callback, page=1, page_size=10)
        self.wait()

    def assert_search_callback(self, response):
        assert response['total'] == 1
        assert len(response['items']) == 1
        assert response['items'][0]['title'] == u'Title'

        self.stop()


    def test_search_query(self):
        self.post_to_elastic_search(self._elastic_search_urls.type_url(Urls.IMAGE_TYPE), {
            'title': u'One', 'createdDate': '2012-10-04T13:00:00'
        })
        self.post_to_elastic_search(self._elastic_search_urls.type_url(Urls.IMAGE_TYPE), {
            'title': u'Two', 'createdDate': '2012-10-04T13:00:00'
        })
    
        self._elastic_search.search(self.assert_search_query_callback, q='One', page=1, page_size=10)
        self.wait()
    
    def assert_search_query_callback(self, response):
        assert response['total'] == 1
        assert response['items'][0]['title'] == u'One'
    
        self.stop()
    
    
    def test_search_created_date_filter(self):
        self.post_to_elastic_search(self._elastic_search_urls.type_url(Urls.IMAGE_TYPE), {
            'title': u'First', 'createdDate': '2012-10-04T13:00:00'
        })
        self.post_to_elastic_search(self._elastic_search_urls.type_url(Urls.IMAGE_TYPE), {
            'title': u'Second', 'createdDate': '2012-10-04T13:00:01'
        })
        self.post_to_elastic_search(self._elastic_search_urls.type_url(Urls.IMAGE_TYPE), {
            'title': u'Third', 'createdDate': '2012-10-04T13:00:02'
        })
        self.post_to_elastic_search(self._elastic_search_urls.type_url(Urls.IMAGE_TYPE), {
            'title': u'Fourth', 'createdDate': '2012-10-04T13:00:03'
        })
    
        self._elastic_search.search(
            self.assert_search_created_date_filter_callback,
            created_date_from=datetime(2012, 10, 4, 13, 0, 1),
            created_date_to=datetime(2012, 10, 4, 13, 0, 2),
            page=1, page_size=10
        )
        self.wait()
    
        self._elastic_search.search(
            self.assert_search_created_date_from_filter_callback,
            created_date_from=datetime(2012, 10, 4, 13, 0, 1),
            page=1, page_size=10
        )
        self.wait()
    
        self._elastic_search.search(
            self.assert_search_created_date_to_filter_callback,
            created_date_to=datetime(2012, 10, 4, 13, 0, 2),
            page=1, page_size=10
        )
        self.wait()
    
    def assert_search_created_date_filter_callback(self, response):
        assert response['total'] == 2
        assert response['items'][0]['title'] == u'Third'
        assert response['items'][1]['title'] == u'Second'
    
        self.stop()
    
    def assert_search_created_date_from_filter_callback(self, response):
        assert response['total'] == 3
        assert response['items'][0]['title'] == u'Fourth'
        assert response['items'][1]['title'] == u'Third'
        assert response['items'][2]['title'] == u'Second'
    
        self.stop()
    
    def assert_search_created_date_to_filter_callback(self, response):
        assert response['total'] == 3
        assert response['items'][0]['title'] == u'Third'
        assert response['items'][1]['title'] == u'Second'
        assert response['items'][2]['title'] == u'First'
    
        self.stop()
    
    
    def test_search_event_date_filter(self):
        self.post_to_elastic_search(self._elastic_search_urls.type_url(Urls.IMAGE_TYPE), {
            'title': u'First', 'eventDate': '2012-10-04T13:00:00', 'createdDate': '2012-10-04T13:00:00'
        })
        self.post_to_elastic_search(self._elastic_search_urls.type_url(Urls.IMAGE_TYPE), {
            'title': u'Second', 'eventDate': '2012-10-04T13:00:01', 'createdDate': '2011-10-04T13:00:00'
        })
        self.post_to_elastic_search(self._elastic_search_urls.type_url(Urls.IMAGE_TYPE), {
            'title': u'Third', 'eventDate': '2012-10-04T13:00:02', 'createdDate': '2010-10-04T13:00:00'
        })
        self.post_to_elastic_search(self._elastic_search_urls.type_url(Urls.IMAGE_TYPE), {
            'title': u'Fourth', 'eventDate': '2012-10-04T13:00:03', 'createdDate': '2009-10-04T13:00:00'
        })
    
        self._elastic_search.search(
            self.assert_search_event_date_filter_callback,
            event_date_from=datetime(2012, 10, 4, 13, 0, 1),
            event_date_to=datetime(2012, 10, 4, 13, 0, 2),
            page=1, page_size=10
        )
        self.wait()
    
        self._elastic_search.search(
            self.assert_search_event_date_from_filter_callback,
            event_date_from=datetime(2012, 10, 4, 13, 0, 1),
            page=1, page_size=10
        )
        self.wait()
    
        self._elastic_search.search(
            self.assert_search_event_date_to_filter_callback,
            event_date_to=datetime(2012, 10, 4, 13, 0, 2),
            page=1, page_size=10
        )
        self.wait()
    
    def assert_search_event_date_filter_callback(self, response):
        assert response['total'] == 2
        assert response['items'][0]['title'] == u'Second'
        assert response['items'][1]['title'] == u'Third'
    
        self.stop()
    
    def assert_search_event_date_from_filter_callback(self, response):
        assert response['total'] == 3
        assert response['items'][0]['title'] == u'Second'
        assert response['items'][1]['title'] == u'Third'
        assert response['items'][2]['title'] == u'Fourth'
    
        self.stop()
    
    def assert_search_event_date_to_filter_callback(self, response):
        assert response['total'] == 3
        assert response['items'][0]['title'] == u'First'
        assert response['items'][1]['title'] == u'Second'
        assert response['items'][2]['title'] == u'Third'
    
        self.stop()
    
    
    def test_search_order_by_relevance_with_query(self):
        self.post_to_elastic_search(self._elastic_search_urls.type_url(Urls.IMAGE_TYPE), {
            'title': u'Exact title', 'createdDate': '2012-10-04T13:00:00'
        })
        self.post_to_elastic_search(self._elastic_search_urls.type_url(Urls.IMAGE_TYPE), {
            'title': u'Title', 'createdDate': '2012-10-05T13:00:00'
        })
    
        self._elastic_search.search(self.assert_search_order_by_relevance_with_query, q='Exact title', page=1, page_size=10)
        self.wait()
    
    def assert_search_order_by_relevance_with_query(self, response):
        assert response['total'] == 2
        assert response['items'][0]['title'] == u'Exact title'
        assert response['items'][1]['title'] == u'Title'
    
        self.stop()
    
    
    def test_search_order_by_newest_first_with_no_query(self):
        self.post_to_elastic_search(self._elastic_search_urls.type_url(Urls.IMAGE_TYPE), {
            'title': u'Exact title', 'createdDate': '2012-10-04T13:00:00'
        })
        self.post_to_elastic_search(self._elastic_search_urls.type_url(Urls.IMAGE_TYPE), {
            'title': u'Title', 'createdDate': '2012-10-05T13:00:00'
        })
    
        self._elastic_search.search(self.assert_search_order_by_newest_first_with_no_query, page=1, page_size=10)
        self.wait()
    
    def assert_search_order_by_newest_first_with_no_query(self, response):
        assert response['total'] == 2
        assert response['items'][0]['title'] == u'Title'
        assert response['items'][1]['title'] == u'Exact title'
    
        self.stop()
    
    
    def test_search_pagination(self):
        self.post_to_elastic_search(self._elastic_search_urls.type_url(Urls.IMAGE_TYPE), {
            'title': u'Title', 'createdDate': '2012-10-04T13:00:00'
        })
        self.post_to_elastic_search(self._elastic_search_urls.type_url(Urls.IMAGE_TYPE), {
            'title': u'Title', 'createdDate': '2012-10-04T13:00:00'
        })
    
        self._elastic_search.search(self.assert_search_pagination_callback_page_1, page=1, page_size=1)
        self.wait()
        self._elastic_search.search(self.assert_search_pagination_callback_page_2, page=2, page_size=1)
        self.wait()
    
    def assert_search_pagination_callback_page_1(self, response):
        assert response['total'] == 2
        assert len(response['items']) == 1
    
        self.stop()
    
    def assert_search_pagination_callback_page_2(self, response):
        assert response['total'] == 2
        assert len(response['items']) == 1
    
        self.stop()
