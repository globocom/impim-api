#!/usr/bin/env python
# -*- coding: utf-8 -*-

from tests.acceptance import BaseImagesAPITestCase

class TestHealthCheckHandlerTestCase(BaseImagesAPITestCase):

    def test_access_to_healthcheck(self):
        response = self.get('/healthcheck')
        self.assertEqual(response.body, "WORKING")

    def test_use_of_querystring(self):
        response = self.get('/healthcheck', my_data=1)
        self.assertTrue(
                response.effective_url.endswith("/healthcheck?my_data=1"))
