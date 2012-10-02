#!/usr/bin/env python
# -*- coding: utf-8 -*-

from unittest import TestCase

from images_api.alpha.infrastructure import ElasticSearchUrls
from tests.support import MockConfig

class ElasticSearchUrlsTestCase(TestCase):
    
    def setUp(self):
        super(ElasticSearchUrlsTestCase, self).setUp()
        self._es_urls = ElasticSearchUrls(config=MockConfig())
    
    def test_index_url(self):
        assert self._es_urls.index_url() == 'http://images:images@esearch.dev.globoi.com/images-test'
    
    def test_type_url(self):
        assert self._es_urls.type_url(ElasticSearchUrls.IMAGE_TYPE) == 'http://images:images@esearch.dev.globoi.com/images-test/image'
    
    def test_search_url(self):
        assert self._es_urls.search_url(ElasticSearchUrls.IMAGE_TYPE) == 'http://images:images@esearch.dev.globoi.com/images-test/image/_search'
    
    def test_refresh_url(self):
        assert self._es_urls.refresh_url() == 'http://images:images@esearch.dev.globoi.com/images-test/_refresh'
