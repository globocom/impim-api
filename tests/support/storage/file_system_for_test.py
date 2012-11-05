#!/usr/bin/env python
# -*- coding: utf-8 -*-


import shutil

from impim_api.domain.storage import FileSystem

from tests.support.mock_config import MockConfig


_file_system = FileSystem(config=MockConfig())

def cleanup():
    shutil.rmtree(_file_system._root_path, ignore_errors=True)
