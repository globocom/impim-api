#!/usr/bin/env python
# -*- coding: utf-8 -*-


import dateutil.parser

from tornado import gen, web
from schema import Use, And
from tapioca import RequestSchema, ParamError, validate, optional

from impim_api.domain.images import Images
from impim_api.handlers import BaseHandler
from impim_api.infrastructure.encoder import JsonDatetimeSerializer, \
        JsonpDatetimeSerializer


not_blank = lambda x: len(x) > 0

class SearchSchema(RequestSchema):
    querystring = {
        optional('q'): unicode,
        optional('created_date_from'): Use(dateutil.parser.parse),
        optional('created_date_to'): Use(dateutil.parser.parse),
        optional('event_date_from'): Use(dateutil.parser.parse),
        optional('event_date_to'): Use(dateutil.parser.parse),
        optional('thumb_sizes', []): Use(lambda s: s.split(',')),
        optional('page', 1): Use(int),
        optional('page_size', 10): (And(Use(int),
            lambda page_size: 1 <= page_size <= 50),
                "The minimum accepted value is 1 and the maximum is 50."),
    }


class ImageCreationSchema(RequestSchema):
    querystring = {
        'title': And(unicode, not_blank),
        'credits': And(unicode, not_blank),
        'tags': Use(lambda argument: [a.strip() for a in argument.split(',')]),
        'event_date': Use(dateutil.parser.parse),
    }


class ImagesResourceHandler(BaseHandler):
    encoders = (JsonDatetimeSerializer, JsonpDatetimeSerializer,)

    def __init__(self, *args, **kwargs):
        super(ImagesResourceHandler, self).__init__(*args, **kwargs)
        self._images = Images(config=self.application.config)

    @validate(SearchSchema)
    @gen.engine
    def get_collection(self, callback):
        result = yield gen.Task(self._images.all, **self.values['querystring'])
        callback(result)

    @gen.engine
    def get_model(self, image_id, callback):
        result = yield gen.Task(self._images.get, image_id=image_id)
        if result is None:
            self.set_status(404)
            self.finish()
        else:
            callback(result)

    @validate(ImageCreationSchema)
    @gen.engine
    def create_model(self, callback):
        try:
            if not 'image' in self.request.files:
                callback(content=['image'])
                return

            image = self.request.files['image'][0]
            result = yield gen.Task(self._images.add, request=self.request,
                    image=image, meta_data=self.values['querystring'])

            location_values = {
                'protocol': self.request.protocol,
                'host': self.request.host,
                'path': self.request.path,
                'id': result['id']
            }
            location = '{protocol}://{host}{path}/{id}'.format(**location_values)

            callback(content=result, location=location)
        except ParamError as e:
            callback(content=[e.param])
