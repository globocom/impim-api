#!/usr/bin/env python
# -*- coding: utf-8 -*-


from datetime import datetime

from tornado import gen

from impim_api.domain import ThumborUrlService
from impim_api.domain.storage import ElasticSearch
from impim_api.domain.storage import TempFileStorage


class Images(object):

    def __init__(self, config, images_storage=None, meta_data_storage=None, thumbor_url_service=None):
        self._images_storage = images_storage or TempFileStorage(config=config)
        self._meta_data_storage = meta_data_storage or ElasticSearch(config=config)
        self._thumbor_url_service = thumbor_url_service or ThumborUrlService(config=config)

    @gen.engine
    def all(self, callback, **search_arguments):
        images_dict = yield gen.Task(self._meta_data_storage.search, **search_arguments)
        for item in images_dict['items']:
            item['thumbs'] = self._thumbor_url_service.fit_in_urls(item['url'], search_arguments.get('thumb_sizes'))
        images_dict['pageSize'] = search_arguments.get('page_size')
        callback(images_dict)

    @gen.engine
    def add(self, callback, image={}, meta_data={}):
        meta_data['created_date'] = datetime.now()
        meta_data['url'] = yield gen.Task(self._images_storage.store_image, **image)
        yield gen.Task(self._meta_data_storage.store_meta_data, **meta_data)
        callback()
