#!/usr/bin/env python
# -*- coding: utf-8 -*-


from libthumbor import CryptoURL
from tornado import gen

from impim_api.domain.storage import ElasticSearch


class ThumborUrlService(object):
    
    # TODO: get thumbor security key from config.
    def fit_in_urls(self, original_url, sizes):
        crypto = CryptoURL(key='MY_SECURE_KEY')
        urls = []
        for size in sizes:
            split_size = size.split('x')
            urls.append({
                size: crypto.generate(image_url=original_url, width=split_size[0], height=split_size[1], fit_in=True)
            })
        return urls
