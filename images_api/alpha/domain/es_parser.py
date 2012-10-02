#!/usr/bin/env python
# -*- coding: utf-8 -*-

import dateutil.parser
from json import dumps, loads

class EsParser(object):
    
    def parse_images_from_search(self, es_json):
        es_data = loads(es_json)
        
        date_fields = ['dataCadastro', 'dataEvento']
        
        photos = []
        for hit in es_data['hits']['hits']:
            photo = {}
            for key in hit['_source'].keys():
                photo[key] = hit['_source'][key]
                if key in date_fields:
                    photo[key] = dateutil.parser.parse(photo[key]).strftime('%d/%m/%Y')
            photos.append(photo)
        
        parsed_data = {
            'total': es_data['hits']['total'],
            'photos': photos,
        }
        
        return parsed_data
