#!/usr/bin/env python
# -*- coding: utf-8 -*-

from unittest import TestCase

from images_api.alpha.infrastructure import EsUrls

class EsParserTestCase(TestCase):
    
    def test_image_search_url(self):
        assert EsUrls.image_search_url() == 'http://esearch.dev.globoi.com/images/image/_search'
