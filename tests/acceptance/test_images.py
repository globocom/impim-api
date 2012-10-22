#!/usr/bin/env python
# -*- coding: utf-8 -*-


from json import loads
from urllib import urlencode

from impim_api.domain.storage.elastic_search import Urls

from tests.support import ElasticSearchMixin
from tests.support import es_cleanup
from tests.support import ImpimAPIAsyncHTTPTestCase
from tests.support import MockConfig


class ImagesTestCase(ImpimAPIAsyncHTTPTestCase, ElasticSearchMixin):

    def setUp(self):
        super(ImagesTestCase, self).setUp()
        self._elastic_search_urls = Urls(MockConfig())
        es_cleanup(self._elastic_search_urls)
        self.post_to_elastic_search(self._elastic_search_urls.type_url(Urls.IMAGE_TYPE), {
            'title': 'Title',
            'url': 's.glbimg.com/et/nv/f/original/2012/09/24/istambul_asia.jpg',
            'createdDate': '2012-10-08T17:02:00',
            'eventDate': '2012-10-08T17:02:00',
        })

    def test_images(self):
        response = self.get('/alpha/images')

        assert response.code == 200, 'the response code should be 200 but it ' \
                                        'was %s' % response.code
        assert 'application/json' in response.headers['Content-Type']
        body = loads(response.body)
        assert body == {
            u'items': [{
                u'title': u'Title',
                u'url': u's.glbimg.com/et/nv/f/original/2012/09/24/istambul_asia.jpg',
                u'eventDate': u'2012-10-08T17:02:00',
                u'createdDate': u'2012-10-08T17:02:00',
                u'thumbs': {},
            }],
            u'total': 1,
            u'pageSize': 10
        }

    def test_images_with_query_string(self):
        query_string = {
            'q': 'Title',
            'created_date_from': '2012-10-08T17:02:00',
            'created_date_to': '2012-10-08T17:02:00',
            'event_date_from': '2012-10-08T17:02:00',
            'event_date_to': '2012-10-08T17:02:00',
            'thumb_sizes': '200x100',
            'page': '1',
            'page_size': '10',
        }
        response = self.get('/alpha/images?%s' % urlencode(query_string))

        assert response.code == 200
        assert 'application/json' in response.headers['Content-Type']
        body = loads(response.body)
        assert body == {
            u'items': [{
                u'title': u'Title',
                u'url': u's.glbimg.com/et/nv/f/original/2012/09/24/istambul_asia.jpg',
                u'eventDate': u'2012-10-08T17:02:00',
                u'createdDate': u'2012-10-08T17:02:00',
                u'thumbs': {'200x100': 'http://localhost:8888/77_UVuSt6igaJ02ShpEISeYgDxk=/fit-in/200x100/s.glbimg.com/et/nv/f/original/2012/09/24/istambul_asia.jpg'},
            }],
            u'total': 1,
            u'pageSize': 10
        }

    def test_images_with_empty_query_string(self):
        response = self.get('/alpha/images?q=&created_date_from=&created_date_to=&event_date_from=&event_date_to=&page=&page_size=')

        assert response.code == 200
        assert 'application/json' in response.headers['Content-Type']
        body = loads(response.body)
        assert body == {
            u'items': [{
                u'title': u'Title',
                u'url': u's.glbimg.com/et/nv/f/original/2012/09/24/istambul_asia.jpg',
                u'eventDate': u'2012-10-08T17:02:00',
                u'createdDate': u'2012-10-08T17:02:00',
                u'thumbs': {},
            }],
            u'total': 1,
            u'pageSize': 10
        }

    def test_images_with_callback(self):
        response = self._fetch(
            self.get_url('/alpha/images?callback=my_images'), 'GET', headers={
                'Accept': 'text/javascript'
            })
        self.assertTrue(response.body.startswith('my_images('))
