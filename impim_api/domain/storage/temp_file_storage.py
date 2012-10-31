#!/usr/bin/env python
# -*- coding: utf-8 -*-


import os


class TempFileStorage(object):
    
    def store_image(self, callback, **image):
        try:
            os.mkdir('/tmp/impim-api')
        except OSError:
            pass
        with open('/tmp/impim-api/%s' % image['filename'], 'w') as image_file:
            image_file.write(image['body'])
            
        callback('http://s.glbimg.com/et/nv/f/original/2012/09/24/istambul_asia.jpg')
