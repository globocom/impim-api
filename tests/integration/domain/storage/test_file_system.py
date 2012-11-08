#!/usr/bin/env python
# -*- coding: utf-8 -*-


import os
from os.path import dirname, join

from mock import MagicMock
from tornado.testing import AsyncTestCase

from impim_api.domain.storage import FileSystem

from tests.support import MockConfig
from tests.support.storage import file_system_for_test


class FileSystemTestCase(AsyncTestCase):

    def setUp(self):
        super(FileSystemTestCase, self).setUp()

        self._storage = FileSystem(MockConfig())
        with open(join(dirname(__file__), '..', '..', '..', 'fixtures/image.jpeg'), 'r') as image_file:
            self._image_body = image_file.read()
        self._image_id = 'id'
        self._request = MagicMock()
        self._request.protocol = 'http'
        self._request.host = 'localhost:8080'

        file_system_for_test.cleanup()

    def test_fetch_image_by_id(self):
        self._storage.store_image(self._fetch_image_by_id_callback, self._image_id, self._request, body=self._image_body, filename='image.jpeg')
        self.wait()
        
    def _fetch_image_by_id_callback(self, url):
        self._storage.fetch_image_by_id(self._fetch_image_by_id_callback_callback, url.split('/')[-2])
        self.wait()
        self.stop()

    def _fetch_image_by_id_callback_callback(self, actual_image_body):
        assert actual_image_body == self._image_body
        self.stop()

    def test_fetch_image_by_id_when_image_does_not_exist(self):
        self._storage.fetch_image_by_id(self._fetch_image_by_id_when_image_does_not_exist_callback, 'non-existent')
        self.wait()

    def _fetch_image_by_id_when_image_does_not_exist_callback(self, actual_image_body):
        assert actual_image_body == None
        self.stop()

    def test_store_image(self):
        self._storage.store_image(self._store_image_callback, self._image_id, self._request, body=self._image_body, filename='image.jpeg')
        self.wait()

    def _store_image_callback(self, url):
        self.assertRegexpMatches(url, r'http://localhost:8080/alpha/images/.+/image\.jpeg')
        self.stop()
