#!/usr/bin/env python
# -*- coding: utf-8 -*-

from datetime import datetime
from json import dumps, loads

from tornado.testing import AsyncTestCase
from tornado.httpclient import AsyncHTTPClient

from images_api.alpha.domain import Images
from images_api.infrastructure.elastic_search import Urls

from tests.support import AsyncHTTPClientMixin
from tests.support import es_cleanup
from tests.support import MockConfig


class ImagesTestCase(AsyncTestCase, AsyncHTTPClientMixin):
    
    def setUp(self):
        super(ImagesTestCase, self).setUp()
        self.http_client = AsyncHTTPClient(self.io_loop)
        self.mock_config = MockConfig()
        self.elastic_search_urls = Urls(self.mock_config)
        self._images = Images(config=self.mock_config, http_client=AsyncHTTPClient(self.io_loop))
        
        es_cleanup(self.elastic_search_urls)

    def test_all(self):
        self._post_to_elastic_search(self.elastic_search_urls.type_url(Urls.IMAGE_TYPE), {
            'title': u'Title'
        })

        self._images.all(self.assert_all_callback, page=1, page_size=10)
        self.wait()

    def assert_all_callback(self, response):
        assert response['total'] == 1
        assert len(response['items']) == 1
        assert response['items'][0]['title'] == u'Title'

        self.stop()


    def test_all_query(self):
        self._post_to_elastic_search(self.elastic_search_urls.type_url(Urls.IMAGE_TYPE), {
            'title': u'One'
        })
        self._post_to_elastic_search(self.elastic_search_urls.type_url(Urls.IMAGE_TYPE), {
            'title': u'Two'
        })
        
        self._images.all(self.assert_all_query_callback, q='One', page=1, page_size=10)
        self.wait()
        
    def assert_all_query_callback(self, response):
        assert response['total'] == 1
        assert response['items'][0]['title'] == u'One'
        
        self.stop()


    def test_all_created_date_filter(self):
        self._post_to_elastic_search(self.elastic_search_urls.type_url(Urls.IMAGE_TYPE), {
            'title': u'First', 'createdDate': '2012-10-04T13:00:00'
        })
        self._post_to_elastic_search(self.elastic_search_urls.type_url(Urls.IMAGE_TYPE), {
            'title': u'Second', 'createdDate': '2012-10-04T13:00:01'
        })
        self._post_to_elastic_search(self.elastic_search_urls.type_url(Urls.IMAGE_TYPE), {
            'title': u'Third', 'createdDate': '2012-10-04T13:00:02'
        })
        self._post_to_elastic_search(self.elastic_search_urls.type_url(Urls.IMAGE_TYPE), {
            'title': u'Fourth', 'createdDate': '2012-10-04T13:00:03'
        })
        
        self._images.all(
            self.assert_all_created_date_filter_callback,
            created_date_from=datetime(2012, 10, 4, 13, 0, 1),
            created_date_to=datetime(2012, 10, 4, 13, 0, 2),
            page=1, page_size=10
        )
        self.wait()
        
        self._images.all(
            self.assert_all_created_date_from_filter_callback,
            created_date_from=datetime(2012, 10, 4, 13, 0, 1),
            page=1, page_size=10
        )
        self.wait()
        
        self._images.all(
            self.assert_all_created_date_to_filter_callback,
            created_date_to=datetime(2012, 10, 4, 13, 0, 2),
            page=1, page_size=10
        )
        self.wait()

    def assert_all_created_date_filter_callback(self, response):
        assert response['total'] == 2
        assert response['items'][0]['title'] == u'Second'
        assert response['items'][1]['title'] == u'Third'

        self.stop()

    def assert_all_created_date_from_filter_callback(self, response):
        assert response['total'] == 3
        assert response['items'][0]['title'] == u'Second'
        assert response['items'][1]['title'] == u'Third'
        assert response['items'][2]['title'] == u'Fourth'

        self.stop()

    def assert_all_created_date_to_filter_callback(self, response):
        assert response['total'] == 3
        assert response['items'][0]['title'] == u'First'
        assert response['items'][1]['title'] == u'Second'
        assert response['items'][2]['title'] == u'Third'

        self.stop()


    def test_all_pagination(self):
        self._post_to_elastic_search(self.elastic_search_urls.type_url(Urls.IMAGE_TYPE), {
            'title': u'Title'
        })
        self._post_to_elastic_search(self.elastic_search_urls.type_url(Urls.IMAGE_TYPE), {
            'title': u'Title'
        })

        self._images.all(self.assert_all_pagination_callback_page_1, page=1, page_size=1)
        self.wait()
        self._images.all(self.assert_all_pagination_callback_page_2, page=2, page_size=1)
        self.wait()

    def assert_all_pagination_callback_page_1(self, response):
        assert response['total'] == 2
        assert response['pageSize'] == 1
        assert len(response['items']) == 1

        self.stop()

    def assert_all_pagination_callback_page_2(self, response):
        assert response['total'] == 2
        assert response['pageSize'] == 1
        assert len(response['items']) == 1

        self.stop()


    def _post_to_elastic_search(self, url, data=''):
        self.post(url, dumps(data))
        self.post(self.elastic_search_urls.refresh_url(), '')
