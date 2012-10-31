#!/usr/bin/env python
# -*- coding: utf-8 -*-


from datetime import datetime, timedelta
from json import loads
from os.path import dirname, join
from urllib import urlencode

import dateutil.parser

from impim_api.domain.storage.elastic_search import Urls

from tests.support import ElasticSearchMixin
from tests.support import ImpimAPIAsyncHTTPTestCase


class ImagesTestCase(ImpimAPIAsyncHTTPTestCase, ElasticSearchMixin):

    def setUp(self):
        super(ImagesTestCase, self).setUp()
        self.post(
            self.get_url('/alpha/images'),
            data=u'title=Title&credits=Créditos&event_date=2012-10-08T17:02:00',
        )
        # image_file = open(join(dirname(__file__), '..', 'fixtures/image.jpeg'), 'rb').read()
        # self.multipart_post(
        #     self.get_url('/alpha/images'),
        #     fields=[('title', 'Title'), ('credits', u'Créditos'), ('event_date', '2012-10-08T17:02:00')],
        #     files=[('image', 'image.jpeg', image_file)]
        # )
        self.refresh_elastic_search()

    def test_images(self):
        response = self.get('/alpha/images')

        assert response.code == 200, 'response code should be 200 but was %s' % response.code
        assert 'application/json' in response.headers['Content-Type']
        body = loads(response.body)
        assert len(body['items']) == 1
        assert body['items'][0]['title'] == u'Title'
        assert body['items'][0]['credits'] == u'Créditos'
        assert body['items'][0]['url'] == u'http://s.glbimg.com/et/nv/f/original/2012/09/24/istambul_asia.jpg'
        assert body['items'][0]['eventDate'] == u'2012-10-08T17:02:00'
        assert isinstance(dateutil.parser.parse(body['items'][0]['createdDate']), datetime)
        assert body['total'] == 1
        assert body['pageSize'] == 10

    def test_images_with_query_string(self):
        query_string = {
            'q': 'Title',
            'created_date_from': (datetime.now() - timedelta(days=1)).isoformat(),
            'created_date_to': (datetime.now() + timedelta(days=1)).isoformat(),
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
        assert len(body['items']) == 1
        assert body['items'][0]['title'] == u'Title'
        assert body['items'][0]['credits'] == u'Créditos'
        assert body['items'][0]['url'] == u'http://s.glbimg.com/et/nv/f/original/2012/09/24/istambul_asia.jpg'
        assert body['items'][0]['eventDate'] == u'2012-10-08T17:02:00'
        assert isinstance(dateutil.parser.parse(body['items'][0]['createdDate']), datetime)
        assert body['items'][0]['thumbs']['200x100'] == u'http://localhost:8888/77_UVuSt6igaJ02ShpEISeYgDxk=/fit-in/200x100/s.glbimg.com/et/nv/f/original/2012/09/24/istambul_asia.jpg'
        assert body['total'] == 1
        assert body['pageSize'] == 10

    def test_images_with_empty_query_string(self):
        response = self.get('/alpha/images?q=&created_date_from=&created_date_to=&event_date_from=&event_date_to=&page=&page_size=')

        assert response.code == 200
        assert 'application/json' in response.headers['Content-Type']
        body = loads(response.body)
        assert len(body['items']) == 1
        assert body['items'][0]['title'] == u'Title'
        assert body['items'][0]['credits'] == u'Créditos'
        assert body['items'][0]['url'] == u'http://s.glbimg.com/et/nv/f/original/2012/09/24/istambul_asia.jpg'
        assert body['items'][0]['eventDate'] == u'2012-10-08T17:02:00'
        assert isinstance(dateutil.parser.parse(body['items'][0]['createdDate']), datetime)
        assert body['items'][0]['thumbs'] == {}
        assert body['total'] == 1
        assert body['pageSize'] == 10

    def test_images_with_callback(self):
        response = self._fetch(
            self.get_url('/alpha/images?callback=my_images'), 'GET', headers={
                'Accept': 'text/javascript'
            })
        self.assertTrue(response.body.startswith('my_images('))
