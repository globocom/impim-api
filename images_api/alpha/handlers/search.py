#!/usr/bin/env python
# -*- coding: utf-8 -*-

from tornado import gen
from tornado.web import asynchronous

from images_api.alpha.domain.images import Images
from images_api.alpha.handlers.base import AlphaBaseHandler


class SearchHandler(AlphaBaseHandler):

    def __init__(self, *args, **kwargs):
        super(SearchHandler, self).__init__(*args, **kwargs)
        self._images = Images(config=self.config)

    @asynchronous
    @gen.engine
    def get(self):
        accepted_arguments = ['page', 'pageSize']
        self.extract_arguments(accepted_arguments)
        response = yield gen.Task(self._images.all)
        self.respond_with(response)
