#!/usr/bin/env python
# -*- coding: utf-8 -*-


from datetime import datetime
from unittest import TestCase

from mock import MagicMock

from impim_api.handlers import ExtractArgumentsMixin


class ExtractArgumentsMixinTestCase(TestCase):

    def setUp(self):
        super(ExtractArgumentsMixinTestCase, self).setUp()
        self.extract_arguments_mixin = ExtractArgumentsMixin()

    def test_extract_arguments_str(self):
        self._mock_get_argument({'str_argument': 'string'})
        
        accepted_arguments = [('str_argument', str, None),]
        arguments = self.extract_arguments_mixin.extract_arguments(accepted_arguments)

        assert arguments['str_argument'] == 'string'

    def test_extract_arguments_int(self):
        self._mock_get_argument({'int_argument': '1'})
        
        accepted_arguments = [('int_argument', int, None),]
        arguments = self.extract_arguments_mixin.extract_arguments(accepted_arguments)

        assert arguments['int_argument'] == 1

    def test_extract_arguments_datetime(self):
        self._mock_get_argument({'datetime_argument': '2012-09-24T14:12:13'})

        accepted_arguments = [('datetime_argument', 'datetime', None),]
        arguments = self.extract_arguments_mixin.extract_arguments(accepted_arguments)

        assert arguments['datetime_argument'] == datetime(2012, 9, 24, 14, 12, 13)

    def test_extract_arguments_list(self):
        self._mock_get_argument({'list_argument': 'first, second'})

        accepted_arguments = [('list_argument', 'list', None),]
        arguments = self.extract_arguments_mixin.extract_arguments(accepted_arguments)

        assert arguments['list_argument'] == ['first', 'second']

    def test_extract_arguments_default(self):
        self._mock_get_argument({})

        accepted_arguments = [('default_argument', str, 'default'),]
        arguments = self.extract_arguments_mixin.extract_arguments(accepted_arguments)

        assert arguments['default_argument'] == 'default'

    def test_extract_arguments_default_none(self):
        self._mock_get_argument({})
        
        accepted_arguments = [('default_argument', str, None),]
        arguments = self.extract_arguments_mixin.extract_arguments(accepted_arguments)

        assert arguments['default_argument'] == None


    def _mock_get_argument(self, arguments):
        def get_argument_returns(argument, default):
            return arguments.get(argument, default)

        self.extract_arguments_mixin.get_argument = MagicMock()
        self.extract_arguments_mixin.get_argument = get_argument_returns