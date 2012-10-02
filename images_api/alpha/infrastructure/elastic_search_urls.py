#!/usr/bin/env python
# -*- coding: utf-8 -*-

from urllib import urlencode

class ElasticSearchUrls(object):
    
    IMAGE_TYPE = 'image'
    
    def __init__(self, config):
        self._config = config
    
    def index_url(self):
        return '%s/%s' % (self._config.ELASTIC_SEARCH_BASE_URL, self._config.ELASTIC_SEARCH_INDEX)
    
    def type_url(self, document_type):
        return '%s/%s' % (self.index_url(), document_type)
    
    def search_url(self, document_type, **kwargs):
        query_string = urlencode(kwargs)
        if query_string:
            query_string = '?%s' % query_string
        return self.type_url(document_type) + '/_search%s' % query_string
        
    def refresh_url(self):
        return "%s/_refresh" % self.index_url()
