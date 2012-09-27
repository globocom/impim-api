#!/usr/bin/env python
# -*- coding: utf-8 -*-

from json import dumps, loads

class EsParser(object):
    
    def parse_images_from_search(self, es_json):
        es_data = loads(es_json)
        
        photos = []
        for hit in es_data['hits']['hits']:
            photos.append({'url': hit['_source']['url']})
        
        parsed_data = {
            'photos': photos
        }
        
        return parsed_data
