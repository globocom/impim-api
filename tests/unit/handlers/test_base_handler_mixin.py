#!/usr/bin/env python
# -*- coding: utf-8 -*-


from unittest import TestCase

from mock import MagicMock

from images_api.handlers import BaseHandlerMixin


class BaseHandlerMixinTestCase(TestCase):
    
    def setUp(self):
        super(BaseHandlerMixinTestCase, self).setUp()
        self._base_handler_mixin = BaseHandlerMixin()
    
    def test_extract_arguments(self):
        def get_argument_returns(argument, default):
            return {
                'page': 1,
                'pageSize': 2
            }.get(argument, default)
        
        self._base_handler_mixin.get_argument = MagicMock()
        self._base_handler_mixin.get_argument = get_argument_returns
        
        accepted_arguments = [('page', None), ('pageSize', None), ('default', 3)]
        arguments = self._base_handler_mixin.extract_arguments(accepted_arguments)
        
        assert arguments['page'] == 1
        assert arguments['page_size'] == 2
        assert arguments['default'] == 3
