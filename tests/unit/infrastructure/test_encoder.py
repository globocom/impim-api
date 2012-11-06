#!/usr/bin/env python
# -*- coding: utf-8 -*-


from datetime import datetime
from unittest import TestCase

from impim_api.infrastructure.encoder import JsonDatetimeSerializer


class JsonEncoderTestCase(TestCase):

    def test_parse_to_string(self):
        encoder = JsonDatetimeSerializer()
        data = {'items': [{'date': datetime(2012, 10, 24)}]}
        assert encoder.datetime_to_string(data) == {'items': [{'date': "2012-10-24T00:00:00"}]}
