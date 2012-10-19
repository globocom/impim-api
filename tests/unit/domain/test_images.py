#!/usr/bin/env python
# -*- coding: utf-8 -*-


from mock import MagicMock
from tornado.httpclient import AsyncHTTPClient
from tornado.testing import AsyncTestCase

from impim_api.domain import Images
from tests.support import MockConfig


class ImagesTestCase(AsyncTestCase):
    
    def setUp(self):
        super(ImagesTestCase, self).setUp()
        self._mock_config = MockConfig()
        self._images = Images(config=self._mock_config, http_client=AsyncHTTPClient(self.io_loop))
    
    def test_images_should_return_page_size(self):
        self._images._es = MagicMock(side_effect=lambda callback, **query_arguments: callback({}))
        self._images.all(self._images_should_return_page_size_callback, page=1, page_size=10)
        self.wait()

    def _images_should_return_page_size_callback(self, response):
        assert response == {'pageSize': 10}
        self.stop()
