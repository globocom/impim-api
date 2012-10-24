#!/usr/bin/env python
# -*- coding: utf-8 -*-


from datetime import datetime
from unittest import TestCase

from impim_api.infrastructure import JsonEncoder


class JsonEncoderTestCase(TestCase):
    
    def test_encode(self):
        encoder = JsonEncoder()
        data = {'date': datetime(2012, 10, 24)}
        assert encoder.encode(data) == '{"date": "2012-10-24T00:00:00"}'
