#!/usr/bin/env python
# -*- coding: utf-8 -*-


from datetime import datetime, timedelta
from json import loads
from urllib import urlencode

import dateutil.parser

from impim_api.domain.storage.elastic_search import Urls

from tests.support import ImpimAPIAsyncHTTPTestCase
from tests.support.factories import ImagesFactory


class GetImagesTestCase(ImpimAPIAsyncHTTPTestCase):

    def setUp(self):
        super(GetImagesTestCase, self).setUp()
        images_factory = ImagesFactory(http_client=self._http_client, images_url=self.get_url('/alpha/images'))
        images_factory.create_image()
        self._elastic_search_for_test.refresh()

    def test_get_images(self):
        response = self._http_client.get('/alpha/images')

        assert response.code == 200, 'response code should be 200 but was %s' % response.code
        assert 'application/json' in response.headers['Content-Type']
        body = loads(response.body)
        assert len(body['items']) == 1
        assert body['items'][0]['title'] == u'Title'
        assert body['items'][0]['credits'] == u'Créditos'
        assert body['items'][0]['tags'] == [u'tag1', u'tag2']
        assert body['items'][0]['eventDate'] == u'2012-10-08T17:02:00'
        assert isinstance(dateutil.parser.parse(body['items'][0]['createdDate']), datetime)
        self.assertRegexpMatches(body['items'][0]['url'], r'http://localhost:\d+/alpha/images/.+/image\.jpeg')
        assert body['items'][0]['width'] == 134
        assert body['items'][0]['height'] == 84
        assert body['items'][0]['thumbs'] == {}
        assert body['total'] == 1
        assert body['pageSize'] == 10

    def test_get_images_with_query_string(self):
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
        response = self._http_client.get('/alpha/images?%s' % urlencode(query_string))

        assert response.code == 200
        assert 'application/json' in response.headers['Content-Type']
        body = loads(response.body)
        assert len(body['items']) == 1
        assert body['items'][0]['title'] == u'Title'
        assert body['items'][0]['credits'] == u'Créditos'
        assert body['items'][0]['tags'] == [u'tag1', u'tag2']
        assert body['items'][0]['eventDate'] == u'2012-10-08T17:02:00'
        assert isinstance(dateutil.parser.parse(body['items'][0]['createdDate']), datetime)
        self.assertRegexpMatches(body['items'][0]['url'], r'http://localhost:\d+/alpha/images/.+/image\.jpeg')
        assert body['items'][0]['width'] == 134
        assert body['items'][0]['height'] == 84
        self.assertRegexpMatches(body['items'][0]['thumbs']['200x100'], r'http://localhost:8888/.*/fit-in/200x100/.*')
        assert body['total'] == 1
        assert body['pageSize'] == 10

    def test_get_images_with_empty_query_string(self):
        response = self._http_client.get('/alpha/images?q=&created_date_from=&created_date_to=&event_date_from=&event_date_to=&page=&page_size=')

        assert response.code == 200
        assert 'application/json' in response.headers['Content-Type']
        body = loads(response.body)
        assert len(body['items']) == 1
        assert body['items'][0]['title'] == u'Title'
        assert body['items'][0]['credits'] == u'Créditos'
        assert body['items'][0]['tags'] == [u'tag1', u'tag2']
        assert body['items'][0]['eventDate'] == u'2012-10-08T17:02:00'
        assert isinstance(dateutil.parser.parse(body['items'][0]['createdDate']), datetime)
        self.assertRegexpMatches(body['items'][0]['url'], r'http://localhost:\d+/alpha/images/.+/image\.jpeg')
        assert body['items'][0]['width'] == 134
        assert body['items'][0]['height'] == 84
        assert body['items'][0]['thumbs'] == {}
        assert body['total'] == 1
        assert body['pageSize'] == 10

    def test_get_images_with_page_size_more_than_the_accepted(self):
        response = self._http_client.get('/alpha/images?page_size=51')

        assert response.code == 400
        assert 'application/json' in response.headers['Content-Type']
        body = loads(response.body)
        assert body['error'] == 'The "page_size" parameter value is not valid.'

    def test_get_images_with_page_size_less_than_the_accepted(self):
        response = self._http_client.get('/alpha/images?page_size=0')

        assert response.code == 400
        assert 'application/json' in response.headers['Content-Type']
        body = loads(response.body)
        assert body['error'] == 'The "page_size" parameter value is not valid.'


class GetImageTestCase(ImpimAPIAsyncHTTPTestCase):

    def test_get_image(self):
        images_factory = ImagesFactory(http_client=self._http_client, images_url=self.get_url('/alpha/images'))
        response = images_factory.create_image()

        url = response.headers['Location']
        path = '/' + ('/').join(url.split('/')[3:])
        response = self._http_client.get(path)

        assert response.code == 200
        assert 'application/json' in response.headers['Content-Type']
        body = loads(response.body)
        assert body['title'] == u'Title'
        assert body['credits'] == u'Créditos'
        assert body['tags'] == [u'tag1', u'tag2']
        assert body['eventDate'] == u'2012-10-08T17:02:00'
        assert isinstance(dateutil.parser.parse(body['createdDate']), datetime)
        self.assertRegexpMatches(body['url'], r'http://localhost:\d+/alpha/images/.+/image\.jpeg')
        assert body['width'] == 134
        assert body['height'] == 84

    def test_get_image_returns_404(self):
        response = self._http_client.get('/alpha/images/no-image')
        assert response.code == 404
        assert response.body == ''


class PostImagesTestCase(ImpimAPIAsyncHTTPTestCase):

    def test_post_images(self):
        images_factory = ImagesFactory(http_client=self._http_client, images_url=self.get_url('/alpha/images'))
        response = images_factory.create_image()

        assert response.code == 201
        assert 'application/json' in response.headers['Content-Type']
        body = loads(response.body)
        assert body['title'] == u'Title'
        assert body['credits'] == u'Créditos'
        assert body['tags'] == [u'tag1', u'tag2']
        assert body['eventDate'] == u'2012-10-08T17:02:00'
        assert isinstance(dateutil.parser.parse(body['createdDate']), datetime)
        self.assertRegexpMatches(body['url'], r'http://localhost:\d+/alpha/images/.+/image\.jpeg')
        assert body['width'] == 134
        assert body['height'] == 84
