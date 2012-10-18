#!/usr/bin/env python
# -*- coding: utf-8 -*-


from tornado_thumbor_url.handlers import GenerateThumborUrlHandler


class JsonpEnabledThumborUrlHandler(GenerateThumborUrlHandler):

    def flush(self, *args, **kwargs):
        self._original_flush = super(JsonpEnabledThumborUrlHandler, self).flush

    def get(self, *args, **kwargs):
        callback_name = self.get_argument('callback', None)
        if not callback_name:
            callback_name = 'defaultCallback'
        self.write('%s("' % callback_name)
        super(JsonpEnabledThumborUrlHandler, self).get(*args, **kwargs)
        self.write('")')
        self.clear_header('Content-Type')
        self.set_header('Content-Type', 'application/javascript')
        self._original_flush()
        self.flush = self._original_flush
