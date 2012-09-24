#!/usr/bin/env python
# -*- coding: utf-8 -*-

from json import loads
from os.path import abspath, dirname, join

IMAGES_FILE_PATH = abspath(join(dirname(__file__), 'images.json'))

class ImageResource(object):

    def all(self):
        if not hasattr(self, '_images'):
            with open(IMAGES_FILE_PATH) as file_with_images:
                self._images = loads(file_with_images.read())
        return self._images
