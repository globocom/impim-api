#!/usr/bin/env python
# -*- coding: utf-8 -*-

from json import loads

from tests.support import ImpimAPIAsyncHTTPTestCase

class ThumborUrlAsJsonpTestCase(ImpimAPIAsyncHTTPTestCase):

    def test_jsonp_call(self):
        response = self._http_client.get('/thumbor_urls', image_url='http://s.glbimg.com/myimg.jpg')
        assert response.code == 200, 'The response code should be 200 but it was %d' % response.code
        assert response.body.startswith('defaultCallback'), 'The default callback should be defaultCallback but it wasn\'t'
        assert response.headers['Content-type'] == 'application/javascript', 'The content type not expected was "%s"' % response.headers['Content-Type']

    def test_giving_a_callback_name(self):
        response = self._http_client.get('/thumbor_urls', image_url='http://s.glbimg.com/myimg.jpg', callback='my_own_name')
        assert response.body.startswith('my_own_name'), 'The callback should be my_own_name but it wasn\'t'

    def test_when_an_error_occurs(self):
        response = self._http_client.get('/thumbor_urls', callback='my_callback_when_error')
        assert response.code == 400, 'When an error occurs the response code should be 400 but it was %d' % response.code
        assert response.body.startswith('my_callback_when_error'), 'The callback should be my_callback_when_error but it wasn\'t'
