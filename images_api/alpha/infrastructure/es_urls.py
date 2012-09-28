#!/usr/bin/env python
# -*- coding: utf-8 -*-

class EsUrls(object):
    
    IMAGE_TYPE = 'image'
    
    @classmethod
    def type_url(cls, type):
        return 'http://esearch.dev.globoi.com/images/%s' % type
    
    @classmethod
    def search_url(cls, type):
        return cls.type_url(type) + '/_search'
        