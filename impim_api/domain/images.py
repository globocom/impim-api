#!/usr/bin/env python
# -*- coding: utf-8 -*-


from tornado import gen

from impim_api.domain.storage import ElasticSearch


class Images(object):

    def __init__(self, config, storage=None):
        self._storage = storage or ElasticSearch(config=config)

    @gen.engine
    def all(self, callback, **search_arguments):
        images_dict = yield gen.Task(self._storage.search, **search_arguments)
        # images_dict['thumbs'] = self._thumb_urls.cropped_to_sizes(search_arguments.get('thumb_sizes'))
        images_dict['pageSize'] = search_arguments.get('page_size')
        callback(images_dict)

