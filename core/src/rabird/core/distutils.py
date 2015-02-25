'''
@date 2013-5-10

@author: HongShe Liang <starofrainnight@gmail.com>

'''

#--IMPORT_ALL_FROM_FUTURE--#

import os
import os.path
import shutil
import sys
import fnmatch
import re

# The shutil.copytree() or distutils.dir_util.copy_tree() will happen to report
# error list below if we invoke it again and again ( at least in python 2.7.4 ):
#
# IOError: [Errno 2] No such file or directory: ...
#
# So we have to write our's copy_tree() for that purpose.
#
def __copy_tree(src_dir, dest_dir):
	if not os.path.exists(dest_dir):
		os.makedirs(dest_dir)
		shutil.copystat(src_dir, dest_dir)
		
	for entry in os.listdir(src_dir):
		from_path = os.path.join(src_dir, entry)
		to_path = os.path.join(dest_dir, entry)
		if os.path.isdir(from_path):
			__copy_tree(from_path, to_path)
		else:
			shutil.copy2(from_path, to_path)

##
# A special method for convert all source files to compatible with current
# python version during installation time.
#
def preprocess_sources_for_compatible(source_path, destination_path):
	# tag_line = r'^[ \t\f\v]*#--IMPORT_ALL_FROM_FUTURE--#[ \t\f\v]*$'
	tag_line =  r'[\r\n][ \t\f\v]*#--IMPORT_ALL_FROM_FUTURE--#[ \t\f\v]*(?:(?:\r\n)|\r|\n)'
	
	# The 'build' and 'dist' folder sometimes will not update! So we need to 
	# remove them all !
	shutil.rmtree(os.path.join(destination_path, 'build'), ignore_errors=True)
	shutil.rmtree(os.path.join(destination_path, 'dist'), ignore_errors=True)
	
	# Remove all unused directories
	directories = []
	directory_patterns = ['__pycache__', '*.egg-info']
	for root, dirs, files in os.walk(destination_path):
		for adir in dirs:
			for pattern in directory_patterns:
				if fnmatch.fnmatch(adir, pattern):
					directories.append(os.path.join(root, adir))
					break
					
	for adir in directories:
		shutil.rmtree(adir, ignore_errors=True)
	
	# Removed old preprocessed sources.
	directories = []
	for item in os.listdir(source_path):
		path = os.path.join(source_path, item)
		if os.path.isdir(path):
			directories.append(item)
			destination_item_path = os.path.join(destination_path, item)
			shutil.rmtree(destination_item_path, ignore_errors=True)
			__copy_tree(path, destination_item_path)
			
	if sys.version_info[0] >= 3:
		# We wrote program implicated by version 3, if python version large or equal than 3,
		# we need not change the sources.
		return
		
	for folder_name in directories:
		for root, dirs, files in os.walk(os.path.join(destination_path, folder_name)):
			for afile in files:
				if fnmatch.fnmatch(afile, '*.py') or fnmatch.fnmatch(afile, '*.pyw'):					
					file_path = os.path.join(root, afile)
					source_file = open(file_path, 'rb+')
					content = source_file.read()
					match = re.search(tag_line, content, re.MULTILINE)
					if match is not None:
						source_file.seek(0) # Go to beginning of file ...
						source_file.write(content[:match.start() + 1]) # All things before tag line
						# Import all future stuffs while we are using python 2.7.x
						source_file.write('from __future__ import nested_scopes\n')
						source_file.write('from __future__ import generators\n')
						source_file.write('from __future__ import division\n')
						source_file.write('from __future__ import absolute_import\n')
						source_file.write('from __future__ import with_statement\n')
						source_file.write('from __future__ import print_function\n')
						source_file.write('from __future__ import unicode_literals\n')
						source_file.write('range = xrange\n') # Emulate behaviors of range
						# Import all exceptions that new introduced in python 3
						source_file.write('from rabird.core.exceptions import *\n')
						source_file.write(content[match.end():]) # Rest after tag line
					source_file.close()
