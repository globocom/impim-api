#!/usr/bin/env python
# -*- coding: utf-8 -*-


from json import dumps


class ElasticSearchMixin(object):
    
    def post_to_elastic_search(self, url, data):
        self.post(url, dumps(data))
        self.post(self._elastic_search_urls.refresh_url(), '')