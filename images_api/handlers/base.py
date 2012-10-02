#!/usr/bin/python
# -*- coding: utf-8 -*-

import json
import tornado.web

from images_api.handlers import BaseHandlerMixin

class BaseHandler(tornado.web.RequestHandler, BaseHandlerMixin):

    @property
    def config(self):
        return self.application.config


class ApiResourceHandler(BaseHandler):

    def encode(self, data):
        return json.dumps(data)

    def decode(self, data):
        return json.loads(data)

    # Generic API HTTP Verbs

    def get(self, *args):
        """ return the collection or a model """
        if self.is_get_collection(*args):
            self.write(self.encode(self.get_collection(*args)))
        else:
            model = self.get_model(*args)
            if model:
                self.write(self.encode(model))
            else:
                raise tornado.web.HTTPError(404)

    def post(self, *args):
        """ create a model """
        resp = self.create_model(self.decode(self.request.body), *args)
        self.write(json.dumps(resp))

    def put(self, *args):
        """ update a model """
        resp = self.update_model(self.decode(self.request.body), *args)
        self.write(json.dumps(resp))

    def delete(self, *args):
        """ delete a model """
        self.delete_model(*args)

    # Extension points

    def is_get_collection(self, *args):
        """ return true if this get is for a collection """
        return len(args) == 0

    def create_model(self, model, *args):
        """ create model and return a dictionary of updated attributes """
        raise tornado.web.HTTPError(404)

    def get_collection(self, *args):
        """ return the collection """
        raise tornado.web.HTTPError(404)

    def get_model(self, *args):
        """ return a model, return None to indicate not found """
        raise tornado.web.HTTPError(404)

    def update_model(self, model, *args):
        """ update a model """
        raise tornado.web.HTTPError(404)

    def delete_model(self, *args):
        """ delete a model """
        raise tornado.web.HTTPError(404)

