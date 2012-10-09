#!/usr/bin/env python
# -*- coding: utf-8 -*-


from json import loads
from urllib import urlencode

from images_api.infrastructure.elastic_search import Urls

from tests.support import ElasticSearchMixin
from tests.support import es_cleanup
from tests.support import ImagesAPIAsyncHTTPTestCase
from tests.support import MockConfig


class ImageSearchTestCase(ImagesAPIAsyncHTTPTestCase, ElasticSearchMixin):

    def setUp(self):
        super(ImageSearchTestCase, self).setUp()
        self._elastic_search_urls = Urls(MockConfig())
        es_cleanup(self._elastic_search_urls)
        self.post_to_elastic_search(self._elastic_search_urls.type_url(Urls.IMAGE_TYPE), {
            'title': 'Title',
            'createdDate': '2012-10-08T17:02:00',
            'eventDate': '2012-10-08T17:02:00',
        })

    def test_search(self):
        response = self.get('/alpha/search')

        assert response.code == 200
        assert 'application/json' in response.headers['Content-Type']
        body = loads(response.body)
        assert body == {u'items': [{u'title': u'Title', u'eventDate': u'2012-10-08T17:02:00', u'createdDate': u'2012-10-08T17:02:00'}], u'total': 1, u'pageSize': 10}

    def test_search_with_query_string(self):
        query_string = {
            'q': 'Title',
            'createdDateFrom': '2012-10-08T17:02:00',
            'createdDateTo': '2012-10-08T17:02:00',
            'eventDateFrom': '2012-10-08T17:02:00',
            'eventDateTo': '2012-10-08T17:02:00',
            'page': '1',
            'pageSize': '10',
        }
        response = self.get('/alpha/search?%s' % urlencode(query_string))

        assert response.code == 200
        assert 'application/json' in response.headers['Content-Type']
        body = loads(response.body)
        assert body == {u'items': [{u'title': u'Title', u'eventDate': u'2012-10-08T17:02:00', u'createdDate': u'2012-10-08T17:02:00'}], u'total': 1, u'pageSize': 10}

    def test_search_with_empty_query_string(self):
        response = self.get('/alpha/search?q=&createdDateFrom=&createdDateTo=&eventDateFrom=&eventDateTo=&page=&pageSize=')

        assert response.code == 200
        assert 'application/json' in response.headers['Content-Type']
        body = loads(response.body)
        assert body == {u'items': [{u'title': u'Title', u'eventDate': u'2012-10-08T17:02:00', u'createdDate': u'2012-10-08T17:02:00'}], u'total': 1, u'pageSize': 10}

    def test_search_with_callback(self):
        response = self.get('/alpha/search', callback='my_images')
        self.assertTrue(response.body.startswith('my_images('))
