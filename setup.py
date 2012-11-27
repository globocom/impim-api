#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
from setuptools import setup, find_packages

def readfile(file_name):
    f = open(os.path.join(os.path.dirname(__file__), file_name))
    return f.read()

setup(
    name='impim-api',
    version='0.1.5',
    author='globo.com',
    author_email='lambda@corp.globo.com',
    license = 'MIT',
    url="https://github.com/globocom/impim-api",
    include_package_data=True,
    packages = find_packages(exclude=["tests.*", "tests"]),
    package_dir = {"impim_api": "impim_api"},
    install_requires=[requirement for requirement in readfile('requirements.txt').split('\n') if requirement],
    entry_points = {
        'console_scripts': [
            'impim-api = impim_api.server:main',
            'impim-api-config = impim_api.conf:generate_config',
        ]
    }
)
