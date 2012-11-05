#!/usr/bin/env python
# -*- coding: utf-8 -*-


import shutil

from impim_api.domain.storage import FileStorage

from tests.support.mock_config import MockConfig


_file_storage = FileStorage(config=MockConfig())

def cleanup():
    shutil.rmtree(_file_storage._root_path, ignore_errors=True)
