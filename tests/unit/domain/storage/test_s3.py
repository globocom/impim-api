#!/usr/bin/env python
# -*- coding: utf-8 -*-

from unittest import TestCase
from mock import Mock, MagicMock, patch, ANY
from boto.exception import S3CreateError

from impim_api.domain.storage import S3Storage
from impim_api.exception import ImageException


class S3StorageTestCase(TestCase):

    def setUp(self):
        self.config = Mock()
        self.config.AWS_ACCESS_KEY_ID = 'awsaki'
        self.config.AWS_SECRET_ACCESS_KEY = 'asak'
        self.config.AWS_BUCKET_NAME = 'my_bucket_name'

    @patch('impim_api.domain.storage.s3.S3Connection')
    def test_create_an_connection(self, conn):
        s3 = S3Storage(self.config)
        conn.assert_called_with('awsaki', 'asak')

    @patch('impim_api.domain.storage.s3.S3Connection')
    def test_bucket_already_exists(self, conn_class):
        connection = Mock(name='connnection')
        connection.create_bucket = Mock(side_effect=S3CreateError(1, None, None))
        conn_class.return_value = connection

        s3 = S3Storage(self.config)
        self.assertRaises(ImageException, s3.store_image, lambda x:x, 'image_id', None)
        connection.create_bucket.assert_called_with('my_bucket_name')

    @patch('impim_api.domain.storage.s3.S3Connection')
    @patch('impim_api.domain.storage.s3.Key')
    def test_save_basic_image_date(self, key_class, conn_class):
        bucket = MagicMock(name='bucket')
        callback = MagicMock(name='callback')
        image_fake_file = 'myimagebinarydata'

        connection_instance = MagicMock(name='the instance of connection')
        connection_instance.create_bucket = Mock(return_value=bucket)
        conn_class.return_value = connection_instance

        key_instance = Mock(name='the instance of key')
        key_instance.generate_url = Mock(return_value='http://s3/image_id')
        key_class.return_value = key_instance

        s3 = S3Storage(self.config)
        s3.store_image(callback, 'image_id', None, body=image_fake_file, filename='image.jpg')

        key_class.assert_called_with(bucket, 'image_id')
        key_instance.set_contents_from_file.assert_called_with(image_fake_file)
        key_instance.generate_url.assert_called_with(1200)
        callback.assert_called_with('http://s3/image_id')

    @patch('impim_api.domain.storage.s3.S3Connection')
    @patch('impim_api.domain.storage.s3.Key')
    def test_get_image_by_id(self, key_class, conn_class):
        bucket = MagicMock(name='bucket')
        callback = MagicMock(name='callback')

        connection_instance = MagicMock(name='the instance of connection')
        connection_instance.create_bucket = Mock(return_value=bucket)
        conn_class.return_value = connection_instance

        key_instance = Mock(name='the instance of key')
        key_instance.generate_url = Mock(return_value='http://s3/image_id')
        key_class.return_value = key_instance

        s3 = S3Storage(self.config)
        s3.fetch_image_by_id(callback, 'image_id')

        callback.assert_called_with('http://s3/image_id')
