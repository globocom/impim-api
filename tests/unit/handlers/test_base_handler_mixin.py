#!/usr/bin/env python
# -*- coding: utf-8 -*-


from datetime import datetime
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
                'int': '1',
                'intCamelCase': '2',
                'date': '2012-09-24T14:12:13',
            }.get(argument, default)
        
        self._base_handler_mixin.get_argument = MagicMock()
        self._base_handler_mixin.get_argument = get_argument_returns
        
        accepted_arguments = [
            ('int', int, None),
            ('intCamelCase', int, None),
            ('date', 'datetime', None),
            ('default', int, 3),
            ('strDefaultNone', str, None),
        ]
        arguments = self._base_handler_mixin.extract_arguments(accepted_arguments)
        
        assert arguments['int'] == 1
        assert arguments['int_camel_case'] == 2
        assert arguments['date'] == datetime(2012, 9, 24, 14, 12, 13)
        assert arguments['default'] == 3
        assert arguments['str_default_none'] == None
