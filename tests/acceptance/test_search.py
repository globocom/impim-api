#!/usr/bin/env python
# -*- coding: utf-8 -*-

from json import loads

from tests.acceptance import BaseImagesAPITestCase

class TestImageSearchTestCase(BaseImagesAPITestCase):

    def test_search_without_filters(self):
        response = self.get('/alpha/search')
        self.assertEqual(response.code, 200)
        self.assertTrue('application/json' in response.headers['Content-Type'])
        results = loads(response.body)
        self.assertTrue('photos' in results)

    def test_search_with_callback(self):
        response = self.get('/alpha/search', callback='my_images')
        self.assertTrue(response.body.startswith('my_images('))
