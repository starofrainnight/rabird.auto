'''
Created on 2013-5-10

@author: HongShe Liang <starofrainnight@gmail.com>

'''

import os
import os.path
import shutil
import sys

def preprocess_sources_for_compatible(source_path, destination_path):
	tag_line = r'#--IMPORT_ALL_FROM_FUTURE--#'
	source_file_path = 'source_version.txt'
	
	while os.path.exists(destination_path):
		# If there have any file in 'from_package' newer than source_version_file's 
		# modify time, we do the complete convertion. 
		status = os.stat(destination_path)

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
			
		# We must break here, otherwise we will run into infinite loop
		break 
			
	# The 'build' and 'dist' folder sometimes will not update! So we need to 
	# remove them all !
	shutil.rmtree('build', ignore_errors=True)
	shutil.rmtree('dist', ignore_errors=True)
	shutil.rmtree(destination_path, ignore_errors=True)
	shutil.copytree(source_path, destination_path)
	
	try:
		open(source_file_path, 'rb+').write(bytearray(sys.version_info.major))
	except:
		pass
	
	if sys.version_info.major >= 3:
		# We wrote program implicated by version 3, if python version large or equal than 3,
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
					source_file.write('range = xrange\n') # Emulate behaviors of range
					source_file.write(content[founded_index+len(tag_line):]) # Rest after tag line
				source_file.close()
				
