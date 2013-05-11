'''
Created on 2013-5-10

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
	tag_line = r'^[ \t\f\v]*#--IMPORT_ALL_FROM_FUTURE--#[ \t\f\v]*$'
	source_file_path = os.path.join(destination_path, 'source_version.txt')
	
	while os.path.exists(source_file_path):
		# If there have any file in 'from_package' newer than source_version_file's 
		# modify time, we do the complete convertion. 
		status = os.stat(source_file_path)

		# Read the source version, if the version not equal current python's version,
		# we need do some change
		try:
			source_version = open(source_file_path, 'rb+').read().strip()
			if int(source_version) != sys.version_info.major:
				# Do convert
				break
		except:
			# Do convert
			break

		is_need_convert = False
		for root, dirs, files in os.walk(source_path):
			for afile in files:
				file_path = os.path.join(root, afile)
				if os.stat(file_path).st_mtime > status.st_ctime:
					is_need_convert = True
					break
			
			if is_need_convert:
				break
		
		if not is_need_convert:
			return
			
		# We must break here, otherwise we will run into infinite loop
		break 
			
	# The 'build' and 'dist' folder sometimes will not update! So we need to 
	# remove them all !
	shutil.rmtree('build', ignore_errors=True)
	shutil.rmtree('dist', ignore_errors=True)
	
	directories = []
	for item in os.listdir(source_path):
		path = os.path.join(source_path, item)
		if os.path.isdir(path):
			directories.append(item)
			destination_item_path = os.path.join(destination_path, item)
			shutil.rmtree(destination_item_path, ignore_errors=True)
			__copy_tree(path, destination_item_path)
			
	try:
		open(source_file_path, 'rb+').write(bytearray(sys.version_info.major))
	except:
		pass
	
	if sys.version_info.major >= 3:
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
						source_file.write(content[:match.start()]) # All things before tag line
						# Import all future stuffs while we are using python 2.7.x
						source_file.write('from __future__ import nested_scopes\n')
						source_file.write('from __future__ import generators\n')
						source_file.write('from __future__ import division\n')
						source_file.write('from __future__ import absolute_import\n')
						source_file.write('from __future__ import with_statement\n')
						source_file.write('from __future__ import print_function\n')
						source_file.write('from __future__ import unicode_literals\n')
						source_file.write('range = xrange\n') # Emulate behaviors of range
						source_file.write(content[match.end():]) # Rest after tag line
					source_file.close()
