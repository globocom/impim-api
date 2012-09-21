#!/usr/bin/env python
# -*- coding: utf-8 -*-

from tornado.testing import AsyncHTTPTestCase

from images_api.app import ImagesApplication


class TestHealthCheckHandlerTestCase(AsyncHTTPTestCase):
    def get_app(self):
        return ImagesApplication()

    def test_access_to_healthcheck(self):
        self.http_client.fetch(self.get_url('/healthcheck'), self.stop)
        response = self.wait()
        self.assertEqual(response.body, "WORKING")
