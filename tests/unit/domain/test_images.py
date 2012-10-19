#!/usr/bin/env python
# -*- coding: utf-8 -*-


from mock import MagicMock
from tornado.testing import AsyncTestCase

from impim_api.domain import Images
from impim_api.domain.storage import ElasticSearch

from tests.support import MockConfig


class ImagesTestCase(AsyncTestCase):
    
    def setUp(self):
        super(ImagesTestCase, self).setUp()
        config = MockConfig()
        self._storage = ElasticSearch(config=config)
        self._images = Images(config=config, storage=self._storage)
    
    def test_images_should_return_page_size(self):
        self._storage.search = MagicMock(side_effect=lambda callback, **query_arguments: callback({}))
        self._images.all(self._images_should_return_page_size_callback, page=1, page_size=10)
        self.wait()

    def _images_should_return_page_size_callback(self, response):
        assert response == {'pageSize': 10}
        self.stop()
