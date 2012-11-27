#!/usr/bin/env python
# -*- coding: utf-8 -*-


from datetime import datetime
from StringIO import StringIO
import uuid

from PIL import Image
from tornado import gen

from impim_api.infrastructure import importer
from impim_api.domain import ThumborUrlService
from impim_api.domain.storage import ElasticSearch
from impim_api.domain.storage import FileSystem


class Images(object):

    def __init__(self, config, thumbor_url_service=None):
        self._images_storage = importer.import_class(config.IMAGES_STORAGE)(config=config)
        self._meta_data_storage = importer.import_class(config.METADATA_STORAGE)(config=config)
        self._thumbor_url_service = thumbor_url_service or ThumborUrlService(config=config)

    @gen.engine
    def all(self, callback, **search_arguments):
        images_dict = yield gen.Task(self._meta_data_storage.search, **search_arguments)
        for item in images_dict['items']:
            item['thumbs'] = self._thumbor_url_service.fit_in_urls(item['url'], search_arguments.get('thumb_sizes'))
        images_dict['page_size'] = search_arguments.get('page_size')
        callback(images_dict)

    @gen.engine
    def get(self, callback, image_id):
        image_dict = yield gen.Task(self._meta_data_storage.fetch_meta_data, image_id=image_id)
        callback(image_dict)

    @gen.engine
    def add(self, callback, request, image={}, meta_data={}):
        pil_image = Image.open(StringIO(image['body']))

        image_id = uuid.uuid4().hex

        meta_data['width'], meta_data['height'] = pil_image.size
        meta_data['created_date'] = datetime.now()
        meta_data['url'] = yield gen.Task(self._images_storage.store_image, image_id=image_id, request=request, **image)

        yield gen.Task(self._meta_data_storage.store_meta_data, image_id=image_id, **meta_data)

        meta_data['id'] = image_id
        callback(meta_data)

    @gen.engine
    def get_image(self, callback, image_id):
        image_body = yield gen.Task(self._images_storage.fetch_image_by_id, image_id=image_id)
        callback(image_body)
