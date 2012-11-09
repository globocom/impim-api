#!/usr/bin/env python
# -*- coding: utf-8 -*-


from impim_api.domain.storage.elastic_search import Urls


class ElasticSearchForTest(object):

    def __init__(self, config, http_client):
        self._http_client = http_client
        self._elastic_search_urls = Urls(config)

    def refresh(self):
        self._http_client.post(self._elastic_search_urls.refresh_url(), '')

    def cleanup(self):
        self._http_client.delete(self._elastic_search_urls.index_url())
