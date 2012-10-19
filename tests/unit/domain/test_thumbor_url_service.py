#!/usr/bin/env python
# -*- coding: utf-8 -*-


from unittest import TestCase

from impim_api.domain import ThumborUrlService


class ThumborTestCase(TestCase):
    
    def test_fit_in_urls(self):
        thumbor_url_service = ThumborUrlService()
        urls = thumbor_url_service.fit_in_urls(
            's.glbimg.com/et/nv/f/original/2012/09/24/istambul_asia.jpg', ['200x100', '300x500']
        )
        assert urls['200x100'] == '/77_UVuSt6igaJ02ShpEISeYgDxk=/fit-in/200x100/s.glbimg.com/et/nv/f/original/2012/09/24/istambul_asia.jpg'
        assert urls['300x500'] == '/IR2Yu13fqbRa4N8HfRs7RC2_UPg=/fit-in/300x500/s.glbimg.com/et/nv/f/original/2012/09/24/istambul_asia.jpg'
