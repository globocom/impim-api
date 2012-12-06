#!/usr/bin/env python
# -*- coding: utf-8 -*-


import derpconf.config as config
from derpconf.config import Config


Config.define('APPLICATION_URL', 'http://0.0.0.0:8080', 'The url to access the running application.', 'General')

Config.define('JSONP_CALLBACK', 'impimCallback', 'Default callback for JSONP responses.', 'General')

Config.define('IMAGES_STORAGE', 'impim_api.domain.storage.FileSystem', 'Defines where the images will be stored.', 'General')
Config.define('METADATA_STORAGE', 'impim_api.domain.storage.ElasticSearch', 'Defines where the metadata will be stored.', 'General')

Config.define('ELASTIC_SEARCH_BASE_URL', 'http://localhost:9200', 'ElasticSearch base url.', 'ElasticSearch')
Config.define('ELASTIC_SEARCH_INDEX', 'impim', 'ElasticSearch index.', 'ElasticSearch')

Config.define('FILE_SYSTEM_ROOT_PATH', '/tmp/impim-api', 'File System root path.', 'File System Storage')

Config.define('AWS_ACCESS_KEY_ID', 'xxx', 'The amazon access key.', 'AWS')
Config.define('AWS_SECRET_ACCESS_KEY', 'yyy', 'The amazon secret key.', 'AWS')
Config.define('AWS_BUCKET_NAME', 'my_bucket', 'The S3 bucket name.', 'AWS')

Config.define('THUMBOR_SECURITY_KEY', 'MY_SECURE_KEY', 'Thumbor security key.', 'Thumbor configuration')
Config.define('THUMBOR_SERVER_URL', 'http://localhost:8888/', 'Thumbor server url.', 'Thumbor configuration')


def generate_config():
    config.generate_config()


if __name__ == '__main__':
    generate_config()
