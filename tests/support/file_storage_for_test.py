#!/usr/bin/env python
# -*- coding: utf-8 -*-


import shutil

from impim_api.domain.storage import TempFileStorage


class FileStorageForTest(object):
    
    def __init__(self, file_storage=TempFileStorage()):
        self._file_storage = file_storage
    
    def cleanup(self):
        shutil.rmtree(self._file_storage._root_path, ignore_errors=True)
