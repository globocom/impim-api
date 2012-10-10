#!/usr/bin/env python
# -*- coding: utf-8 -*-

from tornado import gen
from tornado.web import asynchronous

from images_api.domain.images import Images
from images_api.handlers.extract_arguments_mixin import ExtractArgumentsMixin
from images_api.rest_api import ApiResourceHandler

class ImagesHandler(ApiResourceHandler, ExtractArgumentsMixin):

    def __init__(self, *args, **kwarsg):
        super(ImagesHandler, self).__init__(*args, **kwarsg)
        self.images_storage = Images(config=self.application.config)

    @asynchronous
    @gen.engine
    def get_collection(self, callback, *args):
        accepted_arguments = [
            ('q', str, None),
            ('createdDateFrom', 'datetime', None),
            ('createdDateTo', 'datetime', None),
            ('eventDateFrom', 'datetime', None),
            ('eventDateTo', 'datetime', None),
            ('page', int, 1),
            ('pageSize', int, 10)
        ]
        arguments = self.extract_arguments(accepted_arguments)
        images_dict = yield gen.Task(self.images_storage.all, **arguments)
        callback(images_dict)
