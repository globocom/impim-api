#!/usr/bin/python
# -*- coding: utf-8 -*-


from json import dumps

from tapioca import ResourceHandler


class BaseHandler(ResourceHandler):
    
    def __init__(self, *args, **kwargs):
        super(ResourceHandler, self).__init__(*args, **kwargs)
        self.default_callback_name = self.application.config.JSONP_CALLBACK
