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

    def test_extract_arguments(self):
        def get_argument_returns(argument, default):
            return {
                'int': '1',
                'date': '2012-09-24T14:12:13',
            }.get(argument, default)

        self.extract_arguments_mixin.get_argument = MagicMock()
        self.extract_arguments_mixin.get_argument = get_argument_returns

        accepted_arguments = [
            ('int', int, None),
            ('date', 'datetime', None),
            ('default', int, 3),
            ('str_default_none', str, None),
        ]
        arguments = self.extract_arguments_mixin.extract_arguments(accepted_arguments)

        assert arguments['int'] == 1
        assert arguments['date'] == datetime(2012, 9, 24, 14, 12, 13)
        assert arguments['default'] == 3
        assert arguments['str_default_none'] == None
