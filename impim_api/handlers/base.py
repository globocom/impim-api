#!/usr/bin/python
# -*- coding: utf-8 -*-


from json import dumps

from tapioca import ResourceHandler

from impim_api.handlers import ExtractArgumentsMixin


class BaseHandler(ResourceHandler, ExtractArgumentsMixin):
    
    def __init__(self, *args, **kwargs):
        super(ResourceHandler, self).__init__(*args, **kwargs)
        self.default_callback_name = self.application.config.JSONP_CALLBACK
