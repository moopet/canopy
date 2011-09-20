#!/usr/bin/python

import sys, os
from setuptools import setup
from setuptools import find_packages

__author__ = 'Ben, http://github.com/moopet'
__version__ = '0.1'

setup(
	name = 'canopy',
	version = __version__,

	install_requires = ['simplejson'],

	author = 'Ben',
	author_email = '',
	license = 'unknown',
	url = 'http://github.com/moopet/canopy/tree/master',
	keywords = 'Forrst Api Python Wrapper Canopy',
	description = 'Canopy is a Python client that wraps the Forrst API.',
	long_description = open('README.md').read(),
	classifiers = [
		'Development Status :: 1 - Started',
		'Intended Audience :: Developers',
		'License :: OSI Approved :: Unknown',
		'Topic :: Internet'
	]
)