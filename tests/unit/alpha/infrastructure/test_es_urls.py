#!/usr/bin/env python
# -*- coding: utf-8 -*-

from unittest import TestCase

from images_api.alpha.infrastructure import EsUrls

class EsParserTestCase(TestCase):
    
    def test_type_url(self):
        assert EsUrls.type_url(type='image') == 'http://esearch.dev.globoi.com/images/image'
    
    def test_search_url(self):
        assert EsUrls.search_url(type='image') == 'http://esearch.dev.globoi.com/images/image/_search'
