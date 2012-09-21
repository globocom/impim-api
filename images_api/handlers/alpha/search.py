#!/usr/bin/env python
# -*- coding: utf-8 -*-

import tornado.web

from .base import AlphaBaseHandler


class SearchHandler(AlphaBaseHandler):

    @tornado.web.asynchronous
    def get(self):
        self.respond_with({'photos':[]})
