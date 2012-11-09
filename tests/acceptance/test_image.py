#!/usr/bin/env python
# -*- coding: utf-8 -*-


from json import loads
from os.path import dirname, join

from tests.support import ImpimAPIAsyncHTTPTestCase
from tests.support.factories import ImagesFactory


class GetImageTestCase(ImpimAPIAsyncHTTPTestCase):

    def test_get_image(self):
        images_factory = ImagesFactory(http_client=self._http_client, images_url=self.get_url('/alpha/images'))
        image_body = images_factory.create_image_body()
        response = images_factory.create_image()

        url = loads(response.body)['url']
        path = '/' + ('/').join(url.split('/')[3:])
        response = self._http_client.get(path)

        assert response.code == 200
        assert 'image/jpeg' in response.headers['Content-Type']
        assert response.body == image_body

    def test_get_image_returns_404(self):
        response = self._http_client.get('/alpha/images/no-image/image.jpeg')
        assert response.code == 404
        assert response.body == ''
