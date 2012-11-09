#!/usr/bin/env python
# -*- coding: utf-8 -*-


from tests.support import ImpimAPIAsyncHTTPTestCase


class TestHealthCheckHandlerTestCase(ImpimAPIAsyncHTTPTestCase):

    def test_access_to_healthcheck(self):
        response = self._http_client.get('/healthcheck')
        self.assertEqual(response.body, "WORKING")

    def test_use_of_querystring(self):
        response = self._http_client.get('/healthcheck', my_data=1)
        self.assertTrue(
                response.effective_url.endswith("/healthcheck?my_data=1"))
