#!/usr/bin/env python
# -*- coding: utf-8 -*-


import os
import uuid

from impim_api import API_VERSION


class FileStorage(object):

    def __init__(self, config):
        self._root_path = config.FILE_STORAGE_ROOT_PATH

    def store_image(self, callback, request, **image):
        try:
            os.mkdir(self._root_path)
        except OSError:
            pass

        key = uuid.uuid4().hex
        full_path = self._full_path(key)
        with open(full_path, 'w') as image_file:
            image_file.write(image['body'])
        callback(request.protocol + '://' + request.host + '/' + API_VERSION + '/images/' + key + '/' + image['filename'])

    def fetch_image_by_key(self, key):
        with open(self._full_path(key), 'r') as image_file:
            image_file_body = image_file.read()
        return(image_file_body)

    def _full_path(self, key):
        return '%s/%s' % (self._root_path, key)
