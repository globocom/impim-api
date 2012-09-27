#!/usr/bin/env python
# -*- coding: utf-8 -*-

from derpconf.config import Config

Config.define('JSONP_CALLBACK', 'defaultCallback', 'Callback default for JSONP responses.', 'General')

Config.define('ELASTIC_SEARCH_PHOTOS_URL', 'http://esearch.dev.globoi.com/images/image/_search', 'ElasticSearch url to search for photos.', 'Photo Search')

Config.define('THUMBOR_SECURITY_KEY', 'abc', 'The thumbor security key.', 'Thumbor configuration')
Config.define('THUMBOR_SERVER_URL', 'http://localhost:8888/', 'The thumbor server url.', 'Thumbor configuration')

if __name__ == '__main__':
    print Config.get_config_text()

