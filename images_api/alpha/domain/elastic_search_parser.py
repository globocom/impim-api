#!/usr/bin/env python
# -*- coding: utf-8 -*-

import dateutil.parser
from json import dumps, loads

class ElasticSearchParser(object):
    
    def parse_images_from_search(self, es_json):
        es_data = loads(es_json)
        
        date_fields = ['createdDate', 'eventDate']
        
        images = []
        for hit in es_data['hits']['hits']:
            image = {}
            for key in hit['_source'].keys():
                image[key] = hit['_source'][key]
                if key in date_fields:
                    image[key] = dateutil.parser.parse(image[key]).isoformat()
            images.append(image)
        
        parsed_data = {
            'total': es_data['hits']['total'],
            'items': images,
        }
        
        return parsed_data
