#!/usr/bin/env python
# -*- coding: utf-8 -*-

from unittest import TestCase

from images_api.rest_api import TornadoRESTful, ResourceHandler


class TestApiManager(TestCase):

    def setUp(self):
        self.api = TornadoRESTful()

    def test_should_be_possible_to_add_a_handler(self):
        self.api.add_resource('api', ResourceHandler)
        assert (r'/api/?', ResourceHandler) in self.api.get_url_mapping()

    def test_should_generate_a_path_for_access_direcly_an_instance(self):
        self.api.add_resource('comment', ResourceHandler)
        assert (r'/comment/(?P<key>.+)/?', ResourceHandler) in \
                self.api.get_url_mapping()

    def test_should_generate_path_to_handler_return_type_specification(self):
        self.api.add_resource('comment', ResourceHandler)
        assert (r'/comment\.(?P<force_return_type>\w+)', ResourceHandler) in \
                self.api.get_url_mapping()

    def test_should_generate_path_to_handler_return_type_specification(self):
        self.api.add_resource('comment', ResourceHandler)
        assert (r'/comment/(?P<key>[^.]+)\.(?P<force_return_type>\w+)', ResourceHandler) in \
                self.api.get_url_mapping()
