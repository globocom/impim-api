#!/usr/bin/env python
# -*- coding: utf-8 -*-

from json import dumps, loads

from tests import BaseImagesAPITestCase

class ImageSearchTestCase(BaseImagesAPITestCase):
    
    def setUp(self):
        super(ImageSearchTestCase, self).setUp()
        data = {
            'url': 's.glbimg.com/et/nv/f/original/2012/09/24/istambul_asia.jpg',
            'thumbUrl': 'http://local.globo.com:8888/SGVhWvXVXH4HvduSL1f01ZWj6b16SKVBoC59rDy3Nm5YXWVN3JkSEoOsXwy0SRop/s.glbimg.com/et/nv/f/original/2012/09/24/istambul_asia.jpg',
            'largura': 940,
            'altura': 588,
            'titulo': u'Istambul é a única cidade no mundo que fica em dois continentes: Europa e Ásia',
            'creditos': 'Salve Jorge/TV Globo',
            'assunto': 'Istambul Salve Jorge',
            'dataCadastro': '2009-11-15T14:12:12',
            'dataEvento': '2009-11-15T14:12:12',
        }
        self.post('http://esearch.dev.globoi.com/images-test/image', dumps(data))
    
    def test_search_without_filters(self):
        response = self.get('/alpha/search')
        self.assertEqual(response.code, 200)
        self.assertTrue('application/json' in response.headers['Content-Type'])
        results = loads(response.body)
        self.assertTrue('items' in results)

    def test_search_with_callback(self):
        response = self.get('/alpha/search', callback='my_images')
        self.assertTrue(response.body.startswith('my_images('))
