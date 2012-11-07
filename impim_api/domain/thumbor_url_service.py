#!/usr/bin/env python
# -*- coding: utf-8 -*-


from libthumbor import CryptoURL
from tornado import gen


class ThumborUrlService(object):

    def __init__(self, config):
        self._config = config

    def fit_in_urls(self, original_url, sizes):
        crypto = CryptoURL(key=self._config.THUMBOR_SECURITY_KEY)
        unschemed_original_url = original_url.replace('http://', '')
        urls = {}
        for size in sizes:
            split_size = size.split('x')
            path = crypto.generate(image_url=unschemed_original_url, width=split_size[0], height=split_size[1], fit_in=True)
            urls[size] = self._config.THUMBOR_SERVER_URL.rstrip('/') + path
        return urls
