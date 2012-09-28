#!/usr/bin/env python
# -*- coding: utf-8 -*-

class EsUrls(object):
    
    IMAGE_TYPE = 'image'
    
    @classmethod
    def search_url(cls, type):
        return 'http://esearch.dev.globoi.com/images/%s/_search' % type
        