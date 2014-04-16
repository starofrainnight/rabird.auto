#!/usr/bin/env python

from ez_setup import use_setuptools
use_setuptools()

import os
import os.path
import sys
import shutil
import logging
import fnmatch
import rabird.distutils
import rabird.logging
from setuptools import setup, find_packages

from_package = 'src'
to_package = 'rabird'
package_name = 'rabird.automation'

rabird.logging.load_default_config()

# Convert source to v2.x if we are using python 2.x.
rabird.distutils.preprocess_sources_for_compatible(from_package, os.path.realpath(os.curdir))

# Exclude the original source package, only accept the preprocessed package!
our_packages = find_packages(exclude=[from_package, '{}.*'.format(from_package)])

our_requires = []
setup(
	name=package_name,
	version='.'.join(map(str, (0, 0, 7))),
	author='HongShe Liang',
	author_email='starofrainnight@gmail.com',
	url='',
	py_modules=[to_package],
	description='{} utilities'.format(package_name),
	long_description=open('README', 'r').read(),
	classifiers=[
		'Programming Language :: Python :: 2',
		'Programming Language :: Python :: 3',
		'Intended Audience :: Developers',
		'License :: OSI Approved :: BSD License',
		'Topic :: Software Development :: Libraries',
		'Topic :: Utilities',
	],
	install_requires=our_requires,
    packages=our_packages,
    namespace_packages = ['rabird'],
	)

