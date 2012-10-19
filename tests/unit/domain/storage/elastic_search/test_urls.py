#!/usr/bin/env python
# -*- coding: utf-8 -*-


from unittest import TestCase

from impim_api.domain.storage.elastic_search import Urls

from tests.support import MockConfig


class UrlsTestCase(TestCase):
    
    def setUp(self):
        super(UrlsTestCase, self).setUp()
        self._elastic_search_urls = Urls(config=MockConfig())
    
    def test_index_url(self):
        assert self._elastic_search_urls.index_url() == 'http://localhost:9200/impim-test'
    
    def test_type_url(self):
        assert self._elastic_search_urls.type_url(Urls.IMAGE_TYPE) == 'http://localhost:9200/impim-test/image'
    
    def test_search_url(self):
        assert self._elastic_search_urls.search_url(Urls.IMAGE_TYPE, q='search term') == 'http://localhost:9200/impim-test/image/_search?q=search+term'
    
    def test_refresh_url(self):
        assert self._elastic_search_urls.refresh_url() == 'http://localhost:9200/impim-test/_refresh'
