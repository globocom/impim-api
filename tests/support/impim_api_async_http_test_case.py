#!/usr/bin/env python
# -*- coding: utf-8 -*-


from os.path import abspath, dirname, join

from tornado.ioloop import IOLoop
from tornado.testing import AsyncHTTPTestCase

from impim_api.app import ImagesApplication
from impim_api.domain.storage.elastic_search import Urls

from tests.support import AsyncHTTPClientMixin
from tests.support import es_cleanup


class ImpimAPIAsyncHTTPTestCase(AsyncHTTPTestCase, AsyncHTTPClientMixin):
    
    def setUp(self):
        super(ImpimAPIAsyncHTTPTestCase, self).setUp()
        es_cleanup(Urls(self._app.config))
    
    def get_app(self):
        return ImagesApplication(conf_file=abspath(join(dirname(__file__), '..', 'impim_api.test.conf')))
    
    def get_new_ioloop(self):
        return IOLoop.instance()
