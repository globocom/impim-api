#!/usr/bin/env python
# -*- coding: utf-8 -*-


from json import dumps, loads

from images_api.infrastructure.elastic_search import Urls

from tests.support import es_cleanup
from tests.support import ImagesAPIAsyncHTTPTestCase
from tests.support import MockConfig


class ImageSearchTestCase(ImagesAPIAsyncHTTPTestCase):

    def setUp(self):
        super(ImageSearchTestCase, self).setUp()
        self._elastic_search_urls = Urls(MockConfig())
        es_cleanup(self._elastic_search_urls)
        self.post(self._elastic_search_urls.type_url(Urls.IMAGE_TYPE), dumps({'title': u'Title'}))
        self.post(self._elastic_search_urls.refresh_url(), '')

    def test_search(self):
        response = self.get('/alpha/search')

        assert response.code == 200
        assert 'application/json' in response.headers['Content-Type']
        body = loads(response.body)
        assert body == {u'items': [{u'title': u'Title'}], u'total': 1, u'pageSize': 10}

    def test_search_with_callback(self):
        response = self.get('/alpha/search', callback='my_images')
        self.assertTrue(response.body.startswith('my_images('))
