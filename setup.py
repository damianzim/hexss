#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import setuptools

with open('README.md', 'r') as fh:
    long_description = fh.read()

setuptools.setup(
    name='hexss',
    version='0.2.0',
    author='Damian Zimon',
    description='Print file in hex.',
    url='https://github.com/damianzim/hexss',
    long_description=long_description,
    long_description_content_type='text/markdown',
    packages=setuptools.find_packages(),
    entry_point={
        'console_scripts': [
            'hexss = hexss.__main__',
        ],
    },
)
