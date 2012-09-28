#!/usr/bin/env python
# -*- coding: utf-8 -*-

class EsUrls(object):
    
    IMAGE_TYPE = 'image'
    
    def __init__(self, config):
        self._config = config
    
    def type_url(self, type):
        return '%s/%s/%s' % (self._config.ELASTIC_SEARCH_BASE_URL, self._config.ELASTIC_SEARCH_INDEX, type)
    
    def search_url(self, type):
        return self.type_url(type) + '/_search'
