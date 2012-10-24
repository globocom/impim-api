#!/usr/bin/env python
# -*- coding: utf-8 -*-

from json import loads
from unittest import TestCase

from impim_api.domain.storage.elastic_search import Parser

class ParserTestCase(TestCase):

    def setUp(self):
        self._es_parser = Parser()

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
                  "_index" : "impim-api",
                  "_type" : "image",
                  "_id" : "Ngpkqld6T0SftZpL6KnMhA",
                  "_score" : 1.0,
                  "_source" : {
                    "credits": "Salve Jorge/TV Globo",
                    "url": "s.glbimg.com/et/nv/f/original/2012/09/24/istambul_asia.jpg",
                    "created_date": "2012-09-24T14:12:12",
                    "width": 940,
                    "event_date": "2012-09-24T14:12:12",
                    "title": "Istambul é a única cidade no mundo que fica em dois continentes: Europa e Ásia",
                    "height": 588
                  }
                } ]
              }
            }
        """

        parsed = self._es_parser.parse_images_from_search(es_json)

        assert parsed['total'] == 1
        assert len(parsed['items']) == 1
        assert parsed['items'][0]['credits'] == u"Salve Jorge/TV Globo"
        assert parsed['items'][0]['url'] == "s.glbimg.com/et/nv/f/original/2012/09/24/istambul_asia.jpg"
        assert parsed['items'][0]['createdDate'] == "2012-09-24T14:12:12"
        assert parsed['items'][0]['width'] == 940
        assert parsed['items'][0]['eventDate'] == "2012-09-24T14:12:12"
        assert parsed['items'][0]['title'] == u"Istambul é a única cidade no mundo que fica em dois continentes: Europa e Ásia"
        assert parsed['items'][0]['height'] == 588
