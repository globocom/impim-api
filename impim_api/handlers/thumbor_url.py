#!/usr/bin/env python
# -*- coding: utf-8 -*-

from tornado_thumbor_url.handlers import GenerateThumborUrlHandler, \
        HTTP_BAD_REQUEST, ThumborUrlException


class JsonpEnabledThumborUrlHandler(GenerateThumborUrlHandler):

    def get(self, *args, **kwargs):
        self.set_header('Content-Type', 'application/javascript')

        try:
            content = self.thumbor_complete_url()
        except (ThumborUrlException, ValueError, KeyError) as e:
            self.set_status(HTTP_BAD_REQUEST)
            content = e.message

        callback_name = self.get_argument('callback', 'defaultCallback')
        self.write('{0}("{1}");'.format(callback_name, content))
