#!/usr/bin/env python
# -*- coding: utf-8 -*-

from os.path import join

from boto.exception import S3CreateError
from boto.s3.connection import S3Connection, Key

from .base import ImageStorage
from impim_api.exception import ImageException


HOUR = 1200


class S3Storage(ImageStorage):

    def __init__(self, config):
        self.config = config
        self.conn = S3Connection(config.AWS_ACCESS_KEY_ID, config.AWS_SECRET_ACCESS_KEY)

    def store_image(self, callback, image_id, request, body=None, filename=None, **kwargs):
        bucket = self._get_bucket()
        image = Key(bucket, image_id)
        image.set_contents_from_file(body)
        callback(image.generate_url(HOUR))

    def fetch_image_by_id(self, callback, image_id):
        image = Key(self._get_bucket(), image_id)
        callback(image.generate_url(HOUR))

    def _get_bucket(self):
        try:
            return self.conn.create_bucket(self.config.AWS_BUCKET_NAME)
        except S3CreateError:
            raise ImageException()
