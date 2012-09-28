#!/usr/bin/env python
# -*- coding: utf-8 -*-

from tornado import gen
from tornado.web import asynchronous

from images_api.alpha.domain.images import Images
from images_api.alpha.handlers.base import AlphaBaseHandler


class SearchHandler(AlphaBaseHandler):

    @asynchronous
    @gen.engine
    def get(self):
        images = Images()
        response = yield gen.Task(images.all)
        self.respond_with(response)
