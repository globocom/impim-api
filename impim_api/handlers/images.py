#!/usr/bin/env python
# -*- coding: utf-8 -*-

import dateutil.parser

from tornado import gen, web
from schema import Use, Optional
from tapioca import RequestSchema, validate

from impim_api.domain.images import Images
from impim_api.handlers import BaseHandler
from impim_api.infrastructure.json_encoder import JsonDatetimeSerializer, \
        JsonpDatetimeSerializer


class SearchSchema(RequestSchema):
    querystring = {
        Optional('q'): unicode,
        Optional('created_date_from'): Use(dateutil.parser.parse),
        Optional('created_date_to'): Use(dateutil.parser.parse),
        Optional('event_date_from'): Use(dateutil.parser.parse),
        Optional('event_date_to'): Use(dateutil.parser.parse),
        Optional('thumb_sizes'): Use(lambda s: s.split(',')),
        Optional('page'): Use(int),
        Optional('page_size'): Use(int),
    }


class ImageCreationSchema(RequestSchema):
    querystring = {
        'title': unicode,
        'credits': unicode,
        'event_date': Use(dateutil.parser.parse),
    }


class ImagesResourceHandler(BaseHandler):
    encoders = (JsonDatetimeSerializer, JsonpDatetimeSerializer,)

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

    @gen.engine
    @validate(ImageCreationSchema)
    def create_model(self, callback):
        image = self.request.files['image'][0]
        yield gen.Task(self._images.add, image=image, meta_data=self.values['querystring'])
        callback({'id': 1})
