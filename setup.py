#!/usr/bin/env python

from pydgutils_bootstrap import use_pydgutils, download
use_pydgutils()

import os
import os.path
import sys
import shutil
import logging
import fnmatch
import pydgutils
from setuptools import setup, find_packages

package_name = 'rabird.auto'

# Convert source to v2.x if we are using python 2.x.
our_packages, source_dir = pydgutils.process_packages()

our_requires = [
    'rabird.core',
    'pyscreenshot',
    'numpy',
    'scipy',
    'pillow',
    'psutil>=3.2.2',
    'simplejson',
    'lxml',
]

if sys.platform == 'win32':
    our_requires.append('rabird.winio')

    # If don't have opencv support, we require one
    try:
        import cv2
    except ImportError:
        our_requires.append('opencv-python')

long_description = (
    open("README.rst", "r").read()
    + "\n" +
    open("CHANGES.rst", "r").read()
)

setup(
    name=package_name,
    version='.'.join(map(str, (0, 3, 3))),
    author="Hong-She Liang",
    author_email="starofrainnight@gmail.com",
    url="https://github.com/starofrainnight/%s" % package_name,
    description="The cross-platform windows automate library",
    long_description=long_description,
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 2",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: Implementation :: CPython",
        "Framework :: Rabird",
        "Topic :: Software Development :: Libraries",
        "Topic :: Software Development :: Libraries :: Python Modules",
    ],
    install_requires=our_requires,
    package_dir={"": source_dir},
    packages=our_packages,
    namespace_packages=[package_name.split(".")[0]],
    # If we don"t set the zip_safe to False, pip can"t find us.
    zip_safe=False,
)
