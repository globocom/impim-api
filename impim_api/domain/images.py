#!/usr/bin/env python
# -*- coding: utf-8 -*-


from datetime import datetime

from tornado import gen

from impim_api.domain import ThumborUrlService
from impim_api.domain.storage import ElasticSearch
from impim_api.domain.storage import TempFileStorage


class Images(object):

    def __init__(self, config, data_storage=None, metadata_storage=None, thumbor_url_service=None):
        self._data_storage = data_storage or TempFileStorage()
        self._metadata_storage = metadata_storage or ElasticSearch(config=config)
        self._thumbor_url_service = thumbor_url_service or ThumborUrlService(config=config)

    @gen.engine
    def all(self, callback, **search_arguments):
        images_dict = yield gen.Task(self._metadata_storage.search, **search_arguments)
        for item in images_dict['items']:
            item['thumbs'] = self._thumbor_url_service.fit_in_urls(item['url'], search_arguments.get('thumb_sizes'))
        images_dict['pageSize'] = search_arguments.get('page_size')
        callback(images_dict)

    def add(self, **image_arguments):
        image_arguments['created_date'] = datetime.now()
        image_arguments['url'] = self._data_storage.store()
        self._metadata_storage.store(**image_arguments)
