#!/usr/bin/env python
# -*- coding: utf-8 -*-


from json import loads
from os.path import dirname, join

from tests.support import ImpimAPIAsyncHTTPTestCase


class GetImageTestCase(ImpimAPIAsyncHTTPTestCase):

    def test_get_image(self):
        with open(join(dirname(__file__), '..', 'fixtures/image.jpeg'), 'r') as image_file:
            image_body = image_file.read()
        response = self.multipart_post(
            self.get_url('/alpha/images'),
            fields=[('title', u'Title'), ('credits', u'Créditos'), ('event_date', u'2012-10-08T17:02:00')],
            files=[('image', 'image.jpeg', image_body)]
        )

        url = loads(response.body)['url']
        path = '/' + ('/').join(url.split('/')[3:])
        response = self.get(path)

        assert response.code == 200
        assert 'image/jpeg' in response.headers['Content-Type']
        assert response.body == image_body
    