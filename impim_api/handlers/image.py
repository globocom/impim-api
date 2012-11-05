#!/usr/bin/env python
# -*- coding: utf-8 -*-


from tornado import gen, web
from tornado.web import RequestHandler

from impim_api.domain import Images


class ImageHandler(RequestHandler):

    def __init__(self, *args, **kwargs):
        super(ImageHandler, self).__init__(*args, **kwargs)
        self._images = Images(config=self.application.config)

    @web.asynchronous
    @gen.engine
    def get(self, key):
        image = yield gen.Task(self._images.get, key=key)
        self.set_header('Content-Type', 'image/jpeg')
        self.write(image)
        self.finish()