#!/usr/bin/env python
# -*- coding: utf-8 -*-

from tests import BaseImagesAPITestCase

class TestHealthCheckHandlerTestCase(BaseImagesAPITestCase):

    def test_access_to_healthcheck(self):
        response = self.get('/healthcheck')
        self.assertEqual(response.body, "WORKING")
