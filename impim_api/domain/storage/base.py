#!/usr/bin/env python
# -*- coding: utf-8 -*-


class ImageStorage(object):

    def store_image(self, callback, image_id, request, body=None, **kwargs):
        raise NotImplementedError

    def fetch_image_by_id(self, callback, image_id):
        raise NotImplementedError


class MetadataStorage(object):

    def search(self, callback, **search_arguments):
        raise NotImplementedError

    def fetch_meta_data(self, callback, image_id):
        raise NotImplementedError

    def store_meta_data(self, callback, image_id, **meta_data):
        raise NotImplementedError
