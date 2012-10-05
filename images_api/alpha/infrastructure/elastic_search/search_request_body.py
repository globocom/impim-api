#!/usr/bin/env python
# -*- coding: utf-8 -*-


from json import dumps


class SearchRequestBody:
    
    def __init__(self):
        self._body_dict = {'query': {}}
    
    def from_index(self, from_argument):
        self._body_dict['query']['from'] = from_argument
    
    def size(self, size_argument):
        self._body_dict['query']['size'] = size_argument
    
    def query(self, query_argument):
        self._body_dict['query']['query_string'] = {'query': query_argument}
    
    def as_json(self):
        return dumps(self._body_dict)
        