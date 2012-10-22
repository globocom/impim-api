#!/usr/bin/env python
# -*- coding: utf-8 -*-


from tornado import gen

from impim_api.domain import ThumborUrlService
from impim_api.domain.storage import ElasticSearch


class Images(object):

    def __init__(self, config, storage=None, thumbor_url_service=None):
        self._storage = storage or ElasticSearch(config=config)
        self._thumbor_url_service = thumbor_url_service or ThumborUrlService(config=config)

    @gen.engine
    def all(self, callback, **search_arguments):
        images_dict = yield gen.Task(self._storage.search, **search_arguments)
        for item in images_dict['items']:
            item['thumbs'] = self._thumbor_url_service.fit_in_urls(item['url'], search_arguments.get('thumb_sizes'))
        images_dict['pageSize'] = search_arguments.get('page_size')
        callback(images_dict)
