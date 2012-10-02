#!/usr/bin/env python
# -*- coding: utf-8 -*-

from tornado.httpclient import HTTPClient, HTTPError

def es_cleanup(elastic_search_urls):
    try:
        HTTPClient().fetch(elastic_search_urls.index_url(), method='DELETE')
    except HTTPError, e:
        pass
