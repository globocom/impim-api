#!/usr/bin/env python
# -*- coding: utf-8 -*-


from os.path import abspath, dirname, join

from tornado.ioloop import IOLoop
from tornado.testing import AsyncHTTPTestCase

from images_api.alpha.infrastructure import ElasticSearchUrls
from images_api.app import ImagesApplication

from tests.support import AsyncHTTPClientMixin
from tests.support import es_cleanup


class ImagesAPIAsyncHTTPTestCase(AsyncHTTPTestCase, AsyncHTTPClientMixin):
    
    def setUp(self):
        super(ImagesAPIAsyncHTTPTestCase, self).setUp()
        es_cleanup(ElasticSearchUrls(self._app.config))
    
    def get_app(self):
        return ImagesApplication(conf_file=abspath(join(dirname(__file__), '..', '..', 'images_api.test.conf')))
    
    def get_new_ioloop(self):
        return IOLoop.instance()
