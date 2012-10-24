#!/usr/bin/env python
# -*- coding: utf-8 -*-


from tornado import gen, web

from impim_api.domain.images import Images
from impim_api.handlers import BaseHandler


class ImagesResourceHandler(BaseHandler):

    def __init__(self, *args, **kwargs):
        super(ImagesResourceHandler, self).__init__(*args, **kwargs)
        self._images = Images(config=self.application.config)

    @gen.engine
    def get_collection(self, callback):
        accepted_arguments = [
            ('q', str),
            ('created_date_from', 'datetime'),
            ('created_date_to', 'datetime'),
            ('event_date_from', 'datetime'),
            ('event_date_to', 'datetime'),
            ('thumb_sizes', 'list'),
            ('page', int, 1),
            ('page_size', int, 10),
        ]
        arguments = self.extract_arguments(accepted_arguments)
        images_dict = yield gen.Task(self._images.all, **arguments)
        callback(images_dict)

    @web.asynchronous
    @gen.engine
    def post(self):
        import logging
        logging.info('post')
        logging.info(self.request.files['image'][0]['filename'])
        logging.info(self.request.files['image'][0]['content_type'])
        logging.info(self.get_argument('credits'))
        
        accepted_arguments = [
            ('title', unicode),
            ('credits', unicode),
        ]
        arguments = self.extract_arguments(accepted_arguments)
        yield gen.Task(self._images.add, **arguments)
        
        self.set_header('Content-Type', 'application/json')
        self.set_header('Access-Control-Allow-Origin', '*')
        self.write('{}')
        self.finish()
