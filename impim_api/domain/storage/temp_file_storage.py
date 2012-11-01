#!/usr/bin/env python
# -*- coding: utf-8 -*-


import os
import uuid


class TempFileStorage(object):
    
    _root_path = '/tmp/impim-api'
    
    def store_image(self, callback, **image):
        try:
            os.mkdir(self._root_path)
        except OSError:
            pass
        
        full_path_with_filename = '%s/%s' % (self._root_path, uuid.uuid4().hex)
        with open(full_path_with_filename, 'w') as image_file:
            image_file.write(image['body'])
        callback(full_path_with_filename)
