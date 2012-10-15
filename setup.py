#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
from setuptools import setup

def readfile(file_name):
    f = open(os.path.join(os.path.dirname(__file__), file_name))
    return f.read()

setup(
    name='images-api',
    version='0.1.0dev',
    author='globo.com',
    author_email='lambda@corp.globo.com',
    install_requires=[requirement for requirement in readfile('requirements.txt').split('\n') if requirement],
    entry_points = {
        'console_scripts': [
            'images-api = images_api.server:main',
            'images-api-config = images_api.conf:generate_config',
        ]
    }
)
