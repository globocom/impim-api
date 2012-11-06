#!/usr/bin/env python
# -*- coding: utf-8 -*-

import json

from datetime import datetime

from tapioca import JsonEncoder, JsonpEncoder


class JsonDatetimeSerializer(JsonEncoder):
    def __init__(self, handler=None, camel_case_transform=True):
        super(JsonDatetimeSerializer, self).__init__(handler)
        self.camel_case_transform = camel_case_transform

    def encode(self, data):
        data = self.datetime_to_string(data)
        if self.camel_case_transform:
            return super(JsonDatetimeSerializer, self).encode(data)
        else:
            return json.dumps(data)

    def datetime_to_string(self, value):
        if isinstance(value, dict):
            for k, v in value.items():
                value[k] = self.datetime_to_string(v)
        elif isinstance(value, (list, tuple)):
            for i in range(len(value)):
                value[i] = self.datetime_to_string(value[i])
        elif isinstance(value, datetime):
            return value.isoformat()
        return value


class JsonpDatetimeSerializer(JsonDatetimeSerializer, JsonpEncoder):
    def encode(self, data):
        data = self.datetime_to_string(data)
        return JsonpEncoder.encode(self, data)
