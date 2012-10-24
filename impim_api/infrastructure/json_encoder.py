#!/usr/bin/env python
# -*- coding: utf-8 -*-


from datetime import datetime
from json import dumps


class JsonEncoder(object):
    
    def encode(self, data):
        for k, v in data.items():
            if isinstance(v, datetime):
                data[k] = v.isoformat()
        return dumps(data)
