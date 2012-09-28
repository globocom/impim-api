#!/usr/bin/env python
# -*- coding: utf-8 -*-

class EsUrls(object):
    
    IMAGE_TYPE = 'image'
    
    def type_url(self, type):
        return 'http://esearch.dev.globoi.com/images/%s' % type
    
    def search_url(self, type):
        return self.type_url(type) + '/_search'
        