#!/usr/bin/env python
# -*- coding: utf-8 -*-


from json import dumps, loads

from tests.support import ImagesAPIAsyncHTTPTestCase


class ImageSearchTestCase(ImagesAPIAsyncHTTPTestCase):

    def setUp(self):
        super(ImageSearchTestCase, self).setUp()

    def test_search_without_filters(self):
        response = self.get('/alpha/search')
        self.assertEqual(response.code, 200)
        self.assertTrue('application/json' in response.headers['Content-Type'])
        results = loads(response.body)
        self.assertTrue('items' in results)

    def test_search_with_callback(self):
        response = self.get('/alpha/search', callback='my_images')
        self.assertTrue(response.body.startswith('my_images('))
