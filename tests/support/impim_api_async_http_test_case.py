#!/usr/bin/env python
# -*- coding: utf-8 -*-


from os.path import abspath, dirname, join

from tornado.ioloop import IOLoop
from tornado.testing import AsyncHTTPTestCase

from impim_api.app import ImagesApplication

from tests.support import AsyncHTTPClient
from tests.support.storage import ElasticSearchForTest
from tests.support.storage import file_system_for_test


class ImpimAPIAsyncHTTPTestCase(AsyncHTTPTestCase):

    def setUp(self):
        super(ImpimAPIAsyncHTTPTestCase, self).setUp()

        self._http_client = AsyncHTTPClient(self)
        self._elastic_search_for_test = ElasticSearchForTest(self._app.config, self._http_client)

        self._elastic_search_for_test.cleanup()
        file_system_for_test.cleanup()

    def get_app(self):
        return ImagesApplication(conf_file=abspath(join(dirname(__file__), '..', 'impim_api.test.conf')), base_url='')

    def get_new_ioloop(self):
        return IOLoop.instance()
