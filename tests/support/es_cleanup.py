#!/usr/bin/env python
# -*- coding: utf-8 -*-

from tornado.httpclient import HTTPClient, HTTPError

def es_cleanup():
    try:
        HTTPClient().fetch('http://images:images@esearch.dev.globoi.com/images-test', method='DELETE')
    except HTTPError, e:
        pass
