#!/usr/bin/env python
# -*- coding: utf-8 -*-


import os
import uuid


class TempFileStorage(object):
    
    def store_image(self, callback, **image):
        try:
            os.mkdir('/tmp/impim-api')
        except OSError:
            pass
        
        full_path_filename = '/tmp/impim-api/%s' % uuid.uuid4().hex
        with open(full_path_filename, 'w') as image_file:
            image_file.write(image['body'])
        callback(full_path_filename)
