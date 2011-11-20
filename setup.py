#!python

import os
import os.path
import sys
import shutil
from setuptools import setup

rabird_classifiers = [
    "Programming Language :: Python :: 2",
    "Programming Language :: Python :: 3",
    "Intended Audience :: Developers",
    "License :: OSI Approved :: BSD License",
    "Topic :: Software Development :: Libraries",
    "Topic :: Utilities",
]

if (len(sys.argv) >= 2):
	if sys.version_info.major <= 2:
		current_directory = os.getcwdu()
	else:
		current_directory = os.getcwd()

	dst_path = os.path.join(current_directory, u'build', u'lib' )

	try:
		os.makedirs(dst_path)
	except:
		pass

	try:
		shutil.copytree(u'./rabird', os.path.join(dst_path,u'rabird'), True)
	except:
		pass

fp = open("README", "r")
try:
	rabird_long_description = fp.read()
finally:
	fp.close()

setup(name="rabird",
      version="0.0.0.39",
      author="HongShe Liang",
      author_email="starofrainnight@gmail.com",
      url="",
      py_modules=["rabird"],
      description="rabird utilities",
      long_description=rabird_long_description,
      classifiers=rabird_classifiers
      )

