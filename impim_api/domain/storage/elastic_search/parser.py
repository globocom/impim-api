#!/usr/bin/env python
# -*- coding: utf-8 -*-


from json import dumps, loads
import re

import dateutil.parser


# TODO: This parser should return datetimes, not isoformat() string equivalents. See https://github.com/globocom/impim-api/issues/26
class Parser(object):
    
    def parse_images_from_search(self, es_json):
        es_data = loads(es_json)
        
        date_fields = ['created_date', 'event_date']
        
        images = []
        for hit in es_data['hits']['hits']:
            image = {}
            for key in hit['_source'].keys():
                camelized_key = self._camelize(key)
                image[camelized_key] = hit['_source'][key]
                if key in date_fields:
                    image[camelized_key] = dateutil.parser.parse(image[camelized_key]).isoformat()
            images.append(image)
        
        parsed_data = {
            'total': es_data['hits']['total'],
            'items': images,
        }
        
        return parsed_data

    # TODO: Move this to json encoder http://github.com/globocom/tapioca. See https://github.com/globocom/impim-api/issues/25
    def _camelize(self, key):
        return re.sub(r'_(.)', lambda match: match.group(1).upper(), key)
        