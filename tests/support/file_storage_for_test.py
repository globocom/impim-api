#!/usr/bin/env python
# -*- coding: utf-8 -*-


import shutil

from impim_api.domain.storage import TempFileStorage

from tests.support.mock_config import MockConfig


class FileStorageForTest(object):
    
    def __init__(self, file_storage=None):
        self._file_storage = file_storage or TempFileStorage(config=MockConfig())
    
    def cleanup(self):
        shutil.rmtree(self._file_storage._root_path, ignore_errors=True)
