#!/usr/bin/env python
# -*- coding: utf-8 -*-


from json import dumps, loads
import re

import dateutil.parser


class Parser(object):

    def parse_images_from_search(self, es_json):
        es_data = loads(es_json)

        date_fields = ['created_date', 'event_date']

        images = []
        for hit in es_data['hits']['hits']:
            image = {}
            for key in hit['_source'].keys():
                camelized_key = key
                image[camelized_key] = hit['_source'][key]
                if key in date_fields:
                    image[camelized_key] = dateutil.parser.parse(image[camelized_key])
            images.append(image)

        parsed_data = {
            'total': es_data['hits']['total'],
            'items': images,
        }

        return parsed_data
