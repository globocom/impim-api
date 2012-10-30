#!/usr/bin/env python
# -*- coding: utf-8 -*-


from unittest import TestCase

from impim_api.domain import ThumborUrlService

from tests.support import MockConfig


class ThumborTestCase(TestCase):
    
    def setUp(self):
        super(ThumborTestCase, self).setUp()
        self._thumbor_url_service = ThumborUrlService(MockConfig())
    
    def test_fit_in_urls(self):
        urls = self._thumbor_url_service.fit_in_urls(
            'http://s.glbimg.com/et/nv/f/original/2012/09/24/istambul_asia.jpg', ['200x100', '300x500']
        )
        assert urls['200x100'] == 'http://localhost:8888/77_UVuSt6igaJ02ShpEISeYgDxk=/fit-in/200x100/s.glbimg.com/et/nv/f/original/2012/09/24/istambul_asia.jpg'
        assert urls['300x500'] == 'http://localhost:8888/IR2Yu13fqbRa4N8HfRs7RC2_UPg=/fit-in/300x500/s.glbimg.com/et/nv/f/original/2012/09/24/istambul_asia.jpg'
