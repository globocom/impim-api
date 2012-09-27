#!/usr/bin/env python
# -*- coding: utf-8 -*-

from tornado import gen
from tornado.web import asynchronous

from images_api.alpha.handlers.base import AlphaBaseHandler
from images_api.alpha.resources.images import ImageResource


class SearchHandler(AlphaBaseHandler):

    @asynchronous
    @gen.engine
    def get(self):
        image_resource = ImageResource()
        response = yield gen.Task(image_resource.all, self.config.ELASTIC_SEARCH_PHOTOS_URL)
        self.respond_with(response)
