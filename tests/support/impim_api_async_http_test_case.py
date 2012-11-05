#!/usr/bin/env python
# -*- coding: utf-8 -*-


from os.path import abspath, dirname, join

from tornado.ioloop import IOLoop
from tornado.testing import AsyncHTTPTestCase

from impim_api.app import ImagesApplication
from impim_api.domain.storage.elastic_search import Urls

from tests.support import AsyncHTTPClientMixin
from tests.support import ElasticSearchMixin
from tests.support.storage import file_storage_for_test


class ImpimAPIAsyncHTTPTestCase(AsyncHTTPTestCase, AsyncHTTPClientMixin, ElasticSearchMixin):
    
    def setUp(self):
        super(ImpimAPIAsyncHTTPTestCase, self).setUp()
        self._elastic_search_urls = Urls(self._app.config)
        self.cleanup_elastic_search()
        file_storage_for_test.cleanup()
    
    def get_app(self):
        return ImagesApplication(conf_file=abspath(join(dirname(__file__), '..', 'impim_api.test.conf')), base_url='')
    
    def get_new_ioloop(self):
        return IOLoop.instance()
