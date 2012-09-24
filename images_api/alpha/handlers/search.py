#!/usr/bin/env python
# -*- coding: utf-8 -*-

import tornado.web

from images_api.alpha.handlers.base import AlphaBaseHandler
from images_api.alpha.resources.images import ImageResource


class SearchHandler(AlphaBaseHandler):

    @tornado.web.asynchronous
    def get(self):
        image_resource = ImageResource()
        self.respond_with(image_resource.all())
