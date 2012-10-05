#!/usr/bin/env python
# -*- coding: utf-8 -*-


from unittest import TestCase

from images_api.alpha.infrastructure.elastic_search import Urls
from tests.support import MockConfig


class UrlsTestCase(TestCase):
    
    def setUp(self):
        super(UrlsTestCase, self).setUp()
        self._elastic_search_urls = Urls(config=MockConfig())
    
    def test_index_url(self):
        assert self._elastic_search_urls.index_url() == 'http://images:images@esearch.dev.globoi.com/images-test'
    
    def test_type_url(self):
        assert self._elastic_search_urls.type_url(Urls.IMAGE_TYPE) == 'http://images:images@esearch.dev.globoi.com/images-test/image'
    
    def test_search_url(self):
        assert self._elastic_search_urls.search_url(Urls.IMAGE_TYPE, q='search term') == 'http://images:images@esearch.dev.globoi.com/images-test/image/_search?q=search+term'
    
    def test_refresh_url(self):
        assert self._elastic_search_urls.refresh_url() == 'http://images:images@esearch.dev.globoi.com/images-test/_refresh'
