#!/usr/bin/env python
# -*- coding: utf-8 -*-


import dateutil.parser

from tornado import gen, web
from schema import Use
from tapioca import RequestSchema, validate, optional

from impim_api.domain.images import Images
from impim_api.handlers import BaseHandler
from impim_api.infrastructure.json_encoder import JsonDatetimeSerializer, \
        JsonpDatetimeSerializer


class SearchSchema(RequestSchema):
    querystring = {
        optional('q'): unicode,
        optional('created_date_from'): Use(dateutil.parser.parse),
        optional('created_date_to'): Use(dateutil.parser.parse),
        optional('event_date_from'): Use(dateutil.parser.parse),
        optional('event_date_to'): Use(dateutil.parser.parse),
        optional('thumb_sizes', []): Use(lambda s: s.split(',')),
        optional('page', 1): Use(int),
        optional('page_size', 10): Use(int),
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
        result = yield gen.Task(self._images.all, **self.values['querystring'])
        callback(result)

    @gen.engine
    @validate(ImageCreationSchema)
    def create_model(self, callback):
        image = self.request.files['image'][0]
        result = yield gen.Task(self._images.add, request=self.request, image=image, meta_data=self.values['querystring'])
        
        from json import dumps
        self.set_header('Content-Type', 'application/json')
        self.write(dumps(result))
        
        callback({'id': 1})
