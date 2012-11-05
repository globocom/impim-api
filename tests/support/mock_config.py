#!/usr/bin/env python
# -*- coding: utf-8 -*-


from os.path import abspath, dirname, join

from impim_api.conf import Config


class MockConfig(object):

    config = Config.load(path=abspath(join(dirname(__file__), '..', 'impim_api.test.conf')), conf_name='impim_api.test.conf')
    ELASTIC_SEARCH_BASE_URL = config.ELASTIC_SEARCH_BASE_URL
    ELASTIC_SEARCH_INDEX = config.ELASTIC_SEARCH_INDEX
    FILE_SYSTEM_ROOT_PATH = config.FILE_SYSTEM_ROOT_PATH
    THUMBOR_SECURITY_KEY     = config.THUMBOR_SECURITY_KEY
    THUMBOR_SERVER_URL = config.THUMBOR_SERVER_URL
