#!/usr/bin/env python
# -*- coding: utf-8 -*-

from tornado import gen
from tornado.web import asynchronous

from images_api.domain.images import Images
from images_api.handlers.base import BaseHandler


class SearchHandler(BaseHandler):

    def __init__(self, *args, **kwargs):
        super(SearchHandler, self).__init__(*args, **kwargs)
        self._images = Images(config=self.config)

    @asynchronous
    @gen.engine
    def get(self):
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
        images_dict = yield gen.Task(self._images.all, **arguments)
        self.respond_with(images_dict)
