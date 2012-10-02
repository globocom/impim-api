#!/usr/bin/env python
# -*- coding: utf-8 -*-

from urllib import urlencode

class EsUrls(object):
    
    IMAGE_TYPE = 'image'
    
    def __init__(self, config):
        self._config = config
    
    def type_url(self, type):
        return '%s/%s/%s' % (self._config.ELASTIC_SEARCH_BASE_URL, self._config.ELASTIC_SEARCH_INDEX, type)
    
    def search_url(self, type, **kwargs):
        query_string = urlencode(kwargs)
        if query_string:
            query_string = '?%s' % query_string
        return self.type_url(type) + '/_search%s' % query_string
