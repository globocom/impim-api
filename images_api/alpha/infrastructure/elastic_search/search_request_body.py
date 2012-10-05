#!/usr/bin/env python
# -*- coding: utf-8 -*-


from json import dumps


class SearchRequestBody(object):
    
    def __init__(self):
        self._body_dict = {'query': {}}
    
    def from_index(self, from_argument):
        self._body_dict['query']['from'] = from_argument
    
    def size(self, size_argument):
        self._body_dict['query']['size'] = size_argument
    
    def query(self, query_argument):
        self._body_dict['query']['query_string'] = {'query': query_argument}
    
    def range(self, range_argument):
        query_range = self.Range(range_argument)
        self._body_dict['query']['range'] = query_range.range_dict['range']
        return query_range
    
    def as_json(self):
        return dumps(self._body_dict)
    
    
    class Range(object):
        
        def __init__(self, range_argument):
            self._range_argument = range_argument
            self.range_dict = {'range': {self._range_argument: {}}}
        
        def gte(self, gte_argument):
            self.range_dict['range'][self._range_argument]['gte'] = gte_argument
            return self
        
        def lte(self, lte_argument):
            self.range_dict['range'][self._range_argument]['lte'] = lte_argument
            return self
