#!/usr/bin/env python
# -*- coding: utf-8 -*-

from json import loads
from unittest import TestCase

from images_api.alpha.domain import EsParser

class EsParserTestCase(TestCase):
    
    def setUp(self):
        self._es_parser = EsParser()
    
    def test_parse_images_from_search(self):
        es_json = """
            {
              "took" : 2,
              "timed_out" : false,
              "_shards" : {
                "total" : 5,
                "successful" : 5,
                "failed" : 0
              },
              "hits" : {
                "total" : 1,
                "max_score" : 1.0,
                "hits" : [ {
                  "_index" : "images-api",
                  "_type" : "image",
                  "_id" : "Ngpkqld6T0SftZpL6KnMhA",
                  "_score" : 1.0, "_source" : {"url": "s.glbimg.com/et/nv/f/original/2012/09/24/istambul_asia.jpg"}
                } ]
              }
            }
        """
        
        parsed = self._es_parser.parse_images_from_search(es_json)
        
        assert len(parsed['photos']) == 1
        assert parsed['photos'][0]['url'] == 's.glbimg.com/et/nv/f/original/2012/09/24/istambul_asia.jpg'
