#!/usr/bin/env python

import os
import os.path
import sys
import shutil
import logging
import fnmatch
from src import __version__
from setuptools import setup, find_packages

def convert_source(source_path, destination_path):
	tag_line = r'#--IMPORT_ALL_FROM_FUTURE--#'
	
	if os.path.exists(destination_path):
		# If there have any file in 'from_package' newer than source_version_file's 
		# modify time, we do the complete convertion. 
		status = os.stat(destination_path)
		
		is_need_convert = False
		for root, dirs, files in os.walk(from_package):
			for afile in files:
				file_path = os.path.join(root, afile)
				if os.stat(file_path).st_mtime > status.st_ctime:
					is_need_convert = True
					break
			
			if is_need_convert:
				break
		
		if not is_need_convert:
			return
			
	shutil.rmtree(destination_path,  ignore_errors=True)
	shutil.copytree(source_path, destination_path)
	
	if sys.version_info.major != 2:
		# We wrote program implicated by version 3, if python version large than 2,
		# we need not change the sources.
		return
		
	for root, dirs, files in os.walk(destination_path):
		for afile in files:
			if fnmatch.fnmatch(afile, '*.py') or fnmatch.fnmatch(afile, '*.pyw'):
				file_path = os.path.join(root, afile)
				source_file = open(file_path, 'rb+')
				content = source_file.read()
				founded_index = content.find(tag_line)
				if founded_index >= 0:
					source_file.seek(0) # Go to beginning of file ...
					source_file.write(content[0:founded_index]) # All things before tag line
					# Import all future stuffs while we are using python 2.7.x
					source_file.write('from __future__ import nested_scopes\n')
					source_file.write('from __future__ import generators\n')
					source_file.write('from __future__ import division\n')
					source_file.write('from __future__ import absolute_import\n')
					source_file.write('from __future__ import with_statement\n')
					source_file.write('from __future__ import print_function\n')
					source_file.write('from __future__ import unicode_literals\n')
					source_file.write(content[founded_index+len(tag_line):]) # Rest after tag line
				source_file.close()

from_package = 'src'
to_package = 'rabird'

logging.basicConfig(level=logging.INFO)

# Convert source to v2.x if we are using python 3.x.
convert_source(from_package, to_package)

# Exclude the original source package, only accept the preprocessed package!
our_packages = find_packages(exclude=[from_package]) 

our_requires = [
	'six>=1.3.0'
	]

if sys.platform == "win32":
	our_requires.append('pywin32>=218')


setup(
	name=to_package,
	version=__version__,
	author='HongShe Liang',
	author_email='starofrainnight@gmail.com',
	url='',
	py_modules=[to_package],
	description='{} utilities'.format(to_package),
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
    packages = our_packages,
	)

