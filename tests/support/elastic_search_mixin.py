#!/usr/bin/env python
# -*- coding: utf-8 -*-


from json import dumps


class ElasticSearchMixin(object):

    def refresh_elastic_search(self):
        self.post(self._elastic_search_urls.refresh_url(), '')

    def cleanup_elastic_search(self):
        self.delete(self._elastic_search_urls.index_url())
