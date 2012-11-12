#!/usr/bin/env python
# -*- coding: utf-8 -*-


from os import mkdir
from os.path import exists, join

from .base import ImageStorage
from impim_api import API_VERSION


class FileSystem(ImageStorage):

    def __init__(self, config):
        self._root_path = config.FILE_SYSTEM_ROOT_PATH

    def store_image(self, callback, image_id, request, **image):
        self._safe_mkdir(self._root_path)

        full_path = self._full_path(image_id)
        with open(full_path, 'w') as image_file:
            image_file.write(image['body'])

        url_schema = '{request.protocol}://{request.host}/{api_version}/images/{image_id}/{filename}'
        callback(url_schema.format(request=request, api_version=API_VERSION,
            image_id=image_id, filename=image['filename']))

    def fetch_image_by_id(self, callback, image_id):
        full_path = self._full_path(image_id)
        image_file_body = self._safe_read(full_path)
        callback(image_file_body)

    def _full_path(self, image_id):
        return join(self._root_path, image_id)

    def _safe_mkdir(self, path):
        try:
            mkdir(path)
        except OSError:
            pass

    def _safe_read(self, path):
        try:
            with open(path, 'r') as image_file:
                image_file_body = image_file.read()
            return image_file_body
        except IOError:
            return None
