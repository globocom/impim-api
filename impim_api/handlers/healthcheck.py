#!/usr/bin/python
# -*- coding: utf-8 -*-

import tornado.web

from impim_api.handlers.base import BaseHandler

class HealthCheckHandler(BaseHandler):

    @tornado.web.asynchronous
    def get(self):
        self.write('WORKING')
        self.finish()
