#!/usr/bin/env python
# -*- coding: utf-8 -*-


import os
from os.path import dirname, join

from tornado.testing import AsyncTestCase

from impim_api.domain.storage import TempFileStorage

from tests.support import FileStorageForTest
from tests.support import MockConfig


class TempFileStorageTestCase(AsyncTestCase):

    def setUp(self):
        super(TempFileStorageTestCase, self).setUp()

        self._file_storage = TempFileStorage(MockConfig())
        with open(join(dirname(__file__), '..', '..', '..', 'fixtures/image.jpeg'), 'r') as image_file:
            self._image_body = image_file.read()

        FileStorageForTest(self._file_storage).cleanup()

    def test_store_image(self):
        self._file_storage.store_image(self._store_image_callback, body=self._image_body, filename='image.jpeg')
        self.wait()
        
    def _store_image_callback(self, url):
        with open(url, 'r') as actual_image_file:
            actual_image_body = actual_image_file.read()
        assert actual_image_body == self._image_body
        self.stop()
