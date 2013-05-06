#!python

import os
import os.path
import sys
import shutil
from setuptools import setup, find_packages

setup(
	name="rabird",
	version="0.0.0.39",
	author="HongShe Liang",
	author_email="starofrainnight@gmail.com",
	url="",
	py_modules=["rabird"],
	description="rabird utilities",
	long_description=open("README", "r").read(),
	classifiers=[
		"Programming Language :: Python :: 2",
		"Programming Language :: Python :: 3",
		"Intended Audience :: Developers",
		"License :: OSI Approved :: BSD License",
		"Topic :: Software Development :: Libraries",
		"Topic :: Utilities",
	],
    packages = find_packages(),
	)

