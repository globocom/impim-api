#!/usr/bin/env python
# -*- coding: utf-8 -*-


import derpconf.config as config
from derpconf.config import Config


Config.define('JSONP_CALLBACK', 'defaultCallback', 'Callback default for JSONP responses.', 'General')

Config.define('ELASTIC_SEARCH_BASE_URL', 'http://localhost:9200', 'ElasticSearch base url.', 'ElasticSearch')
Config.define('ELASTIC_SEARCH_INDEX', 'images', 'ElasticSearch index.', 'ElasticSearch')

Config.define('THUMBOR_SECURITY_KEY', 'MY_SECURE_KEY', 'The thumbor security key.', 'Thumbor configuration')
Config.define('THUMBOR_SERVER_URL', 'http://localhost:8888/', 'The thumbor server url.', 'Thumbor configuration')


def generate_config():
    config.generate_config()


if __name__ == '__main__':
    generate_config()
