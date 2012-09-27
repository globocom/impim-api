#!/usr/bin/env python
# -*- coding: utf-8 -*-

from json import dumps, loads

class EsParser(object):
    
    def parse_images_from_search(self, es_json):
        es_data = loads(es_json)
        
        photos = []
        for hit in es_data['hits']['hits']:
            photo = {}
            for key in hit['_source'].keys():
                photo[key] = hit['_source'][key]
            photos.append(photo)
        
        parsed_data = {
            'numFound': len(photos),
            'photos': photos,
        }
        
        return parsed_data
