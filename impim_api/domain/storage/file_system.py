#!/usr/bin/env python
# -*- coding: utf-8 -*-


import os

from impim_api import API_VERSION


class FileSystem(object):

    def __init__(self, config):
        self._root_path = config.FILE_SYSTEM_ROOT_PATH

    def store_image(self, callback, image_id, request, **image):
        try:
            os.mkdir(self._root_path)
        except OSError:
            pass

        full_path = self._full_path(image_id)
        with open(full_path, 'w') as image_file:
            image_file.write(image['body'])
        callback(request.protocol + '://' + request.host + '/' + API_VERSION + '/images/' + image_id + '/' + image['filename'])

    def fetch_image_by_id(self, callback, image_id):
        with open(self._full_path(image_id), 'r') as image_file:
            image_file_body = image_file.read()
        callback(image_file_body)

    def _full_path(self, image_id):
        return '%s/%s' % (self._root_path, image_id)
