#!/usr/bin/env python
# -*- coding: utf-8 -*-


from os.path import dirname, join


class ImagesFactory(object):

    def __init__(self, http_client, images_url):
        self._http_client = http_client
        self._images_url = images_url

    def create_image(self):
        with open(join(dirname(__file__), '..', 'fixtures/image.jpeg'), 'r') as image_file:
            image_body = image_file.read()
        return self._http_client.multipart_post(
            self._images_url,
            fields=[('title', u'Title'), ('credits', u'Créditos'), ('event_date', u'2012-10-08T17:02:00')],
            files=[('image', 'image.jpeg', image_body)]
        )