#!/usr/bin/env python
# -*- coding: utf-8 -*-


from json import dumps


class SearchRequestBody(object):
    
    def __init__(self):
        self._body_dict = {}
        self._ranges = {}
    
    def from_index(self, from_argument):
        self._body_dict['from'] = from_argument
    
    def size(self, size_argument):
        self._body_dict['size'] = size_argument
    
    def query_string(self, query_argument):
        self._body_dict['query'] = {'query_string': {'query': query_argument}}
    
    def range(self, range_argument):
        if not self._body_dict.get('query'):
            self._body_dict['query'] = {}
        
        if not self._body_dict['query'].get('range'):
            self._body_dict['query']['range'] = {}
        
        if not self._ranges.get(range_argument):
            self._ranges[range_argument] = self.Range(range_argument)
            self._body_dict['query']['range'][range_argument] = self._ranges[range_argument].range_dict
        
        return self._ranges[range_argument]
    
    def as_json(self):
        return dumps(self._body_dict)
    
    
    class Range(object):
        
        def __init__(self, range_argument):
            self._range_argument = range_argument
            self.range_dict = {}
        
        def gte(self, gte_argument):
            self.range_dict['gte'] = gte_argument
            return self
        
        def lte(self, lte_argument):
            self.range_dict['lte'] = lte_argument
            return self
