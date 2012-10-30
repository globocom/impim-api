#!/usr/bin/env python
# -*- coding: utf-8 -*-

from datetime import datetime

from tornado import gen, web
from schema import Use, Optional
from tapioca import RequestSchema, validate

from impim_api.domain.images import Images
from impim_api.handlers import BaseHandler


class SearchSchema(RequestSchema):
    querystring = {
        Optional('q'): unicode,
        Optional('created_date_from'): Use(datetime),
        Optional('created_date_to'): Use(datetime),
        Optional('event_date_from'): Use(datetime),
        Optional('event_date_to'): Use(datetime),
        Optional('thumb_sizes'): Use(lambda s: s.split(',')),
        Optional('page'): Use(int),
        Optional('page_size'): Use(int),
    }


class ImagesResourceHandler(BaseHandler):

    def __init__(self, *args, **kwargs):
        super(ImagesResourceHandler, self).__init__(*args, **kwargs)
        self._images = Images(config=self.application.config)

    @gen.engine
    @validate(SearchSchema)
    def get_collection(self, callback):
        values = self.values['querystring']
        if not 'page' in values:
            values['page'] = 1
        if not 'page_size' in values:
            values['page_size'] = 10
        if not 'thumb_sizes' in values:
            values['thumb_sizes'] = []
        images_dict = yield gen.Task(self._images.all, **values)
        callback(images_dict)

    @web.asynchronous
    @gen.engine
    def post(self):
        accepted_arguments = [
            ('title', unicode),
            ('credits', unicode),
            ('created_date', 'datetime'),
            ('event_date', 'datetime'),
        ]
        arguments = self.extract_arguments(accepted_arguments)
        yield gen.Task(self._images.add, **arguments)

        self.set_header('Content-Type', 'application/json')
        self.set_header('Access-Control-Allow-Origin', '*')
        self.write('{}')
        self.finish()
