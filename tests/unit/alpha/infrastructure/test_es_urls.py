#!/usr/bin/env python
# -*- coding: utf-8 -*-

from unittest import TestCase

from images_api.alpha.infrastructure import EsUrls
from tests.support import MockConfig

class EsParserTestCase(TestCase):
    
    def setUp(self):
        super(EsParserTestCase, self).setUp()
        self._es_urls = EsUrls(config=MockConfig())
    
    def test_type_url(self):
        assert self._es_urls.type_url('image') == 'http://images:images@esearch.dev.globoi.com/images-test/image'
    
    def test_search_url(self):
        assert self._es_urls.search_url('image') == 'http://images:images@esearch.dev.globoi.com/images-test/image/_search'
