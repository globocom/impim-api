#!/usr/bin/env python
# -*- coding: utf-8 -*-

from json import dumps, loads

from tornado.testing import AsyncTestCase
from tornado.httpclient import AsyncHTTPClient

from images_api.alpha.domain import Images
from images_api.alpha.infrastructure import ElasticSearchUrls

from tests.support import AsyncHTTPClientMixin
from tests.support import es_cleanup
from tests.support import MockConfig


class ImagesTestCase(AsyncTestCase, AsyncHTTPClientMixin):
    
    def setUp(self):
        super(ImagesTestCase, self).setUp()
        self.http_client = AsyncHTTPClient(self.io_loop)
        self.mock_config = MockConfig()
        self.elastic_search_urls = ElasticSearchUrls(self.mock_config)
        
        es_cleanup(self.elastic_search_urls)

    def test_all(self):
        self._post_to_elastic_search(self.elastic_search_urls.type_url(ElasticSearchUrls.IMAGE_TYPE), {
            'titulo': u'Título'
        })

        images = Images(config=self.mock_config, http_client=AsyncHTTPClient(self.io_loop))
        images.all(self.assert_all_callback)
        self.wait()

    def assert_all_callback(self, response):
        assert response['total'] == 1
        assert len(response['items']) == 1
        assert response['items'][0]['titulo'] == u'Título'

        self.stop()

    def test_all_pagination(self):
        self._post_to_elastic_search(self.elastic_search_urls.type_url(ElasticSearchUrls.IMAGE_TYPE), {
            'titulo': u'Título'
        })
        self._post_to_elastic_search(self.elastic_search_urls.type_url(ElasticSearchUrls.IMAGE_TYPE), {
            'titulo': u'Título'
        })

        images = Images(config=self.mock_config, http_client=self.http_client)
        images.all(self.assert_all_pagination_callback_page_1, page=1, page_size=1)
        self.wait()
        images.all(self.assert_all_pagination_callback_page_2, page=2, page_size=1)
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
