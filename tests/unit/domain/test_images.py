#!/usr/bin/env python
# -*- coding: utf-8 -*-


from datetime import datetime
from os.path import dirname, join

from mock import ANY, MagicMock, patch
from tornado.testing import AsyncTestCase

from impim_api.domain import Images

from tests.support import MockConfig


class ImagesTestCase(AsyncTestCase):

    @patch('impim_api.domain.storage.FileSystem')
    @patch('impim_api.domain.storage.ElasticSearch')
    def setUp(self, elastic_search_class, filesystem_class):
        super(ImagesTestCase, self).setUp()

        config = MockConfig()
        config.IMAGES_STORAGE = 'impim_api.domain.storage.FileSystem'
        config.METADATA_STORAGE = 'impim_api.domain.storage.ElasticSearch'

        self._thumbor_url_service = MagicMock()
        self._meta_data_storage = MagicMock()
        self._images_storage = MagicMock()

        filesystem_class.return_value = self._images_storage
        elastic_search_class.return_value = self._meta_data_storage

        self._images = Images(config=config, thumbor_url_service=self._thumbor_url_service)

    def test_all(self):
        self._meta_data_storage.search = MagicMock(side_effect=lambda callback, **query_arguments: callback({
            'items': [{'url': 'http://s.glbimg.com/et/nv/f/original/2012/09/24/istambul_asia.jpg'}]
        }))
        self._thumbor_url_service.fit_in_urls = MagicMock(return_value={'200x100': 'http://localhost:8888/77_UVuSt6igaJ02ShpEISeYgDxk=/fit-in/200x100/s.glbimg.com/et/nv/f/original/2012/09/24/istambul_asia.jpg'})

        self._images.all(
            self._all_callback,
            thumb_sizes=['200x100'],
            page=1,
            page_size=10
        )
        self.wait()

    def _all_callback(self, response):
        assert response['items'][0]['url'] == 'http://s.glbimg.com/et/nv/f/original/2012/09/24/istambul_asia.jpg'
        assert response['items'][0]['thumbs']['200x100'] == 'http://localhost:8888/77_UVuSt6igaJ02ShpEISeYgDxk=/fit-in/200x100/s.glbimg.com/et/nv/f/original/2012/09/24/istambul_asia.jpg'
        assert response['page_size'] == 10
        self.stop()

    def test_get(self):
        self._meta_data_storage.fetch_meta_data = MagicMock(side_effect=lambda callback, image_id: callback({
            'url': 'http://s.glbimg.com/et/nv/f/original/2012/09/24/istambul_asia.jpg'
        }))
        self._images.get(self._get_callback, 'image_id')
        self.wait()

    def _get_callback(self, response):
        assert response['url'] == 'http://s.glbimg.com/et/nv/f/original/2012/09/24/istambul_asia.jpg'
        self.stop()

    def test_add(self):
        with open(join(dirname(__file__), '..', '..', 'fixtures/image.jpeg'), 'r') as image_file:
            image_body = image_file.read()

        with patch('impim_api.domain.images.datetime') as mock_datetime:
            mock_datetime.now.return_value = datetime(2012, 10, 25, 18, 55, 0)
            self._images_storage.store_image = MagicMock(side_effect=lambda callback, request, **kwargs: callback(
                'http://s.glbimg.com/et/nv/f/original/2012/09/24/istambul_asia.jpg'
            ))
            self._meta_data_storage.store_meta_data = MagicMock(side_effect=lambda callback, **image_meta_data: callback())

            self._images.add(self._add_callback, request=None, image={'body': image_body}, meta_data={'title': u'image title'})
            self.wait()

    def _add_callback(self, result_meta_data):
        self._images_storage.store_image.assert_called_with(callback=ANY, image_id=ANY, request=None, body=ANY)
        self._meta_data_storage.store_meta_data.assert_called_with(
            callback=ANY,
            image_id=ANY,
            title=u'image title',
            created_date=datetime(2012, 10, 25, 18, 55, 0),
            url='http://s.glbimg.com/et/nv/f/original/2012/09/24/istambul_asia.jpg',
            width=134,
            height=84
        )

        assert result_meta_data['id'] is not None
        assert result_meta_data['title'] == 'image title'
        assert isinstance(result_meta_data['created_date'], datetime)
        assert result_meta_data['url'] == 'http://s.glbimg.com/et/nv/f/original/2012/09/24/istambul_asia.jpg'
        assert result_meta_data['width'] == 134
        assert result_meta_data['height'] == 84

        self.stop()

    def test_get_image(self):
        with open(join(dirname(__file__), '..', '..', 'fixtures/image.jpeg'), 'r') as image_file:
            image_body = image_file.read()
        self._images_storage.fetch_image_by_id = MagicMock(return_value=image_body)

        self._images.get_image(self._get_image_callback, image_id='image_id') == image_body

    def _get_image_callback(self, actual_image_body):
        with open(join(dirname(__file__), '..', '..', 'fixtures/image.jpeg'), 'r') as image_file:
            image_body = image_file.read()
        assert actual_image_body == image_body
