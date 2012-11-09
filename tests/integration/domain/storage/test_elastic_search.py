#!/usr/bin/env python
# -*- coding: utf-8 -*-


from datetime import datetime
from json import dumps, loads
import uuid

from tornado.httpclient import AsyncHTTPClient
from tornado.testing import AsyncTestCase

from impim_api.domain.storage import ElasticSearch
from impim_api.domain.storage.elastic_search import Urls

from tests.support import AsyncHTTPClient as TestAsyncHTTPClient
from tests.support import MockConfig
from tests.support.storage import ElasticSearchForTest


class ElasticSearchTestCase(AsyncTestCase):

    def setUp(self):
        super(ElasticSearchTestCase, self).setUp()

        config = MockConfig()

        self._http_client = AsyncHTTPClient(self.io_loop)
        self._test_http_client = TestAsyncHTTPClient(self)
        self._elastic_search_urls = Urls(config)
        self._elastic_search = ElasticSearch(config=config, http_client=self._http_client)
        self._elastic_search_for_test = ElasticSearchForTest(config=config, http_client=self._test_http_client)

        self._elastic_search_for_test.cleanup()

    def test_search(self):
        self._elastic_search.store_meta_data(self._noop_callback, 'id1', title=u'Title')
        self.wait()
        self._elastic_search_for_test.refresh()

        self._elastic_search.search(self.assert_search_callback, page=1, page_size=10)
        self.wait()

    def assert_search_callback(self, response):
        assert response['total'] == 1
        assert len(response['items']) == 1
        assert response['items'][0]['title'] == u'Title'

        self.stop()


    def test_search_query(self):
        self._elastic_search.store_meta_data(self._noop_callback, 'id1', title=u'One')
        self.wait()
        self._elastic_search.store_meta_data(self._noop_callback, 'id2', title=u'Two')
        self.wait()
        self._elastic_search_for_test.refresh()

        self._elastic_search.search(self.assert_search_query_callback, q='One', page=1, page_size=10)
        self.wait()

    def assert_search_query_callback(self, response):
        assert response['total'] == 1
        assert response['items'][0]['title'] == u'One'

        self.stop()


    def test_search_created_date_filter(self):
        self._elastic_search.store_meta_data(self._noop_callback, 'id1', title=u'First', created_date=datetime(2012, 10, 4, 13, 0, 3))
        self.wait()
        self._elastic_search.store_meta_data(self._noop_callback, 'id2', title=u'Second', created_date=datetime(2012, 10, 4, 13, 0, 2))
        self.wait()
        self._elastic_search.store_meta_data(self._noop_callback, 'id3', title=u'Third', created_date=datetime(2012, 10, 4, 13, 0, 1))
        self.wait()
        self._elastic_search.store_meta_data(self._noop_callback, 'id4', title=u'Fourth', created_date=datetime(2012, 10, 4, 13, 0, 0))
        self.wait()
        self._elastic_search_for_test.refresh()

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
        assert response['items'][0]['title'] == u'Second'
        assert response['items'][1]['title'] == u'Third'

        self.stop()

    def assert_search_created_date_from_filter_callback(self, response):
        assert response['total'] == 3
        assert response['items'][0]['title'] == u'First'
        assert response['items'][1]['title'] == u'Second'
        assert response['items'][2]['title'] == u'Third'

        self.stop()

    def assert_search_created_date_to_filter_callback(self, response):
        assert response['total'] == 3
        assert response['items'][0]['title'] == u'Second'
        assert response['items'][1]['title'] == u'Third'
        assert response['items'][2]['title'] == u'Fourth'

        self.stop()


    def test_search_event_date_filter(self):
        self._elastic_search.store_meta_data(self._noop_callback, 'id1', title=u'First', event_date=datetime(2012, 10, 4, 13, 0, 3), created_date=datetime(2012, 10, 4, 13, 0, 3))
        self.wait()
        self._elastic_search.store_meta_data(self._noop_callback, 'id2', title=u'Second', event_date=datetime(2012, 10, 4, 13, 0, 2), created_date=datetime(2012, 10, 4, 13, 0, 2))
        self.wait()
        self._elastic_search.store_meta_data(self._noop_callback, 'id3', title=u'Third', event_date=datetime(2012, 10, 4, 13, 0, 1), created_date=datetime(2012, 10, 4, 13, 0, 1))
        self.wait()
        self._elastic_search.store_meta_data(self._noop_callback, 'id4', title=u'Fourth', event_date=datetime(2012, 10, 4, 13, 0, 0), created_date=datetime(2012, 10, 4, 13, 0, 0))
        self.wait()
        self._elastic_search_for_test.refresh()

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
        assert response['items'][0]['title'] == u'First'
        assert response['items'][1]['title'] == u'Second'
        assert response['items'][2]['title'] == u'Third'

        self.stop()

    def assert_search_event_date_to_filter_callback(self, response):
        assert response['total'] == 3
        assert response['items'][0]['title'] == u'Second'
        assert response['items'][1]['title'] == u'Third'
        assert response['items'][2]['title'] == u'Fourth'

        self.stop()


    def test_search_order_by_relevance_with_query(self):
        self._elastic_search.store_meta_data(self._noop_callback, 'id1', title=u'Exact title')
        self.wait()
        self._elastic_search.store_meta_data(self._noop_callback, 'id2', title=u'Title')
        self.wait()
        self._elastic_search_for_test.refresh()

        self._elastic_search.search(self.assert_search_order_by_relevance_with_query, q='Exact title', page=1, page_size=10)
        self.wait()

    def assert_search_order_by_relevance_with_query(self, response):
        assert response['total'] == 2
        assert response['items'][0]['title'] == u'Exact title'
        assert response['items'][1]['title'] == u'Title'

        self.stop()


    def test_search_order_by_newest_first_with_no_query(self):
        self._elastic_search.store_meta_data(self._noop_callback, 'id1', title=u'Exact title', created_date=datetime(2012, 10, 4, 13, 0, 0))
        self.wait()
        self._elastic_search.store_meta_data(self._noop_callback, 'id2', title=u'Title', created_date=datetime(2012, 10, 5, 13, 0, 0))
        self.wait()
        self._elastic_search_for_test.refresh()

        self._elastic_search.search(self.assert_search_order_by_newest_first_with_no_query, page=1, page_size=10)
        self.wait()

    def assert_search_order_by_newest_first_with_no_query(self, response):
        assert response['total'] == 2
        assert response['items'][0]['title'] == u'Title'
        assert response['items'][1]['title'] == u'Exact title'

        self.stop()


    def test_search_pagination(self):
        self._elastic_search.store_meta_data(self._noop_callback, 'id1', title=u'Title')
        self.wait()
        self._elastic_search.store_meta_data(self._noop_callback, 'id2', title=u'Title')
        self.wait()
        self._elastic_search_for_test.refresh()

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


    def test_fetch_meta_data(self):
        image_id = 'id'
        self._elastic_search.store_meta_data(self._noop_callback, image_id)
        self.wait()
        
        self._elastic_search.fetch_meta_data(self.assert_fetch_meta_data, image_id)
        self.wait()

    def assert_fetch_meta_data(self, response):
        assert response['id'] == u'id'
        self.stop()


    def _noop_callback(self):
        self.stop()
