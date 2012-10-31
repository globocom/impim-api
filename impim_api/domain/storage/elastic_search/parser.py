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
            image = hit['_source']
            for key in image:
                if key in date_fields:
                    image[key] = dateutil.parser.parse(image[key])
            images.append(image)
        return {
            'total': es_data['hits']['total'],
            'items': images,
        }
