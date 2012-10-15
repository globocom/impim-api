#!/usr/bin/env python
# -*- coding: utf-8 -*-


from os.path import abspath, dirname, join

from images_api.conf import Config


class MockConfig(object):

    config = Config.load(path=abspath(join(dirname(__file__), '..', 'images_api.test.conf')), conf_name='images_api.test.conf')
    ELASTIC_SEARCH_BASE_URL = config.ELASTIC_SEARCH_BASE_URL
    ELASTIC_SEARCH_INDEX = config.ELASTIC_SEARCH_INDEX
