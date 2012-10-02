#!/usr/bin/env python
# -*- coding: utf-8 -*-

from json import dumps, loads
from tornado.httpclient import AsyncHTTPClient
from tornado.testing import AsyncTestCase

from images_api.alpha.domain import Images
from tests.support import MockConfig

class ImagesTestCase(AsyncTestCase):
    
    def test_all(self):
        http_client = AsyncHTTPClient(self.io_loop)
        
        http_client.fetch('http://images:images@esearch.dev.globoi.com/images-test', self.stop, method='DELETE')
        self.wait()
        
        data = {
            'titulo': u'Título',
        }
        http_client.fetch('http://esearch.dev.globoi.com/images-test/image', self.stop, method='POST', body=dumps(data))
        self.wait()
        http_client.fetch('http://images:images@esearch.dev.globoi.com/images-test/_flush', self.stop, method='POST', body='')
        self.wait()
        
        images = Images(config=MockConfig(), http_client=AsyncHTTPClient(self.io_loop))
        
        images.all(self._all_callback)
        self.wait()
    
    def _all_callback(self, response):
        assert response['total'] == 1
        assert len(response['photos']) == 1
        assert response['photos'][0]['titulo'] == u'Título'
        
        self.stop()
    
    def test_all_pagination(self):
        http_client = AsyncHTTPClient(self.io_loop)
        
        http_client.fetch('http://images:images@esearch.dev.globoi.com/images-test', self.stop, method='DELETE')
        self.wait()

        data = {
            'titulo': u'Título',
        }
        http_client.fetch('http://esearch.dev.globoi.com/images-test/image', self.stop, method='POST', body=dumps(data))
        self.wait()
        data = {
            'titulo': u'Título',
        }
        http_client.fetch('http://esearch.dev.globoi.com/images-test/image', self.stop, method='POST', body=dumps(data))
        self.wait()
        http_client.fetch('http://images:images@esearch.dev.globoi.com/images-test/_flush', self.stop, method='POST', body='')
        self.wait()

        images = Images(config=MockConfig(), http_client=http_client)
        images.all(self._all_pagination_callback_page_1, page=1, page_size=1)
        self.wait()
        images.all(self._all_pagination_callback_page_2, page=2, page_size=1)
        self.wait()

    def _all_pagination_callback_page_1(self, response):
        assert response['total'] == 2
        assert len(response['photos']) == 1

        self.stop()

    def _all_pagination_callback_page_2(self, response):
        assert response['total'] == 2
        assert len(response['photos']) == 1

        self.stop()
