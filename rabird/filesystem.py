# -*- coding: UTF-8 -*-

## A module unified all file system related stuffs. 
# 
# @note We have read_symbolic_link() implementation, but do not have a 
# read_hard_link() implementation and related stuffs. why? Because the hard link
# just linked to the file object and do not record the original path, though 
# each hard link will be target to the same object, but it just act like a real
# file without original path we linked to. So ...
#  
# @date: 2011-11-13
# @author: starofrainnight

import rabird.compatible
import os
import sys
import shutil

# Python 2.x in win32 do not support link operations, so we use jaraco.window to
# add this support.
if (sys.version_info.major <= 2) and (sys.platform == "win32"):
	import win32api
	import win32file
	
	version = win32api.GetVersionEx(0)
	
	# Vista or above, we use CreateSymbolicLink() to implement our symlink().
	if (version[0] >= 6) and (version >= 0):
		def __symlink(from_path, to_symbol_link_path):
			if os.path.isdir(from_path):
				win32api.CreateSymbolicLink(from_path, to_symbol_link_path, 1)
			else:
				win32api.CreateSymbolicLink(from_path, to_symbol_link_path, 0)
	else:
		def __symlink(from_path, to_symbol_link_path):
			raise NotImplementedError(
				'Only support create symbolic link on Vista or above!')
				
	# Win2000 or above:
	# we use CreateHardLink() to implement our link() and use 
	# GetFileAttributes() to implement our islink().
	if (version[0] >= 5) and (version >= 0):
		def __link(from_path, to_hard_link_path):
			win32file.CreateHardLink(from_path, to_hard_link_path)
			
		def __islink(path):
			# 0x400 == FILE_ATTRIBUTE_REPARSE_POINT
			return win32file.GetFileAttributes() & 0x400  
	else:
		def __link(from_path, to_hard_link_path):
			raise NotImplementedError(
				'Only support create hard link on Win2000 or above!')
			
		def __islink(path):
			raise NotImplementedError(
				'Only support check link status on Win2000 or above!')
		
	if not hasattr(os, 'symlink'):
		os.symlink = __symlink
		os.path.islink = __islink
		
	def __readlink(path):
		raise NotImplementedError(
			'Only support check link status on Win2000 or above!')
		
	if not hasattr(os, 'readlink'):
		os.readlink = __readlink
		
	if not hasattr(os, 'link'):
		os.link = __link
		
class option_t(object):
	NONE = 0
	
	## If we do recursive on directories? Only effect on directory operation.
	# Note : It only effect on directory remove operation.
	RECURSIVE = 1
	
	## Ignored any errors we met when we doing an operation.
	IGNORE_ERRORS = 2
	
	## Unused
	FORCE = 4
	
	## Follow symbolic links when doing copy operations
	FOLLOW_SYMBOLIC_LINKS = 8
	
class path_t(rabird.compatible.unicode_t):
	def __init__(self, path=u""):
		super(path_t, self).__init__()
		
		## Internal path string, must be in unicode format.
		self.__path = unicode(path)
	
	## Support str(path object) or unicode(path object), they are all return
	# an unicode object, actually rabird library is only support unicode 
	# string!
	def __unicode__(self):
		return self.__path
	
	def __div__(self, rhs):
		return path_t(os.path.join(self.__path, unicode(rhs))) 
				
	def clear(self):
		self.__path = u""
	
	def make_preferred(self):
		self.__path = os.path.normpath(self.__path)
		return self

def change_current_path(path):
	os.chdir(unicode(path))
		
def create_directories(path):
	os.makedirs(unicode(path))
	
def create_directory(path):
	os.mkdir(unicode(path))

## Create a hard link ( unimplemented )
def create_hard_link(from_path, to_hard_link_path):
	os.link(unicode(from_path), unicode(to_hard_link_path))

## Create a symbolic link ( unimplemented )
def create_symbolic_link(from_path, to_symbol_link_path):
	os.symlink(unicode(from_path), unicode(to_symbol_link_path))

def copy(from_path, to_path, options = option_t.NONE ):
	from_path = unicode(from_path)
	to_path = unicode(to_path)
	if is_directory(from_path):
		shutil.copytree(
			from_path, 
			to_path, 
			not (options & option_t.FOLLOW_SYMBOLIC_LINKS) )
	else:
		shutil.copy2(from_path, to_path)

def read_symbolic_link(path):
	os.readlink(unicode(path))

## Remove target path 
#
# @param [in] path: Target path we need to remove
# @param [in] options: A series options to control the remove behaviors.
# @see option_t.
# @param [in] on_error: A callable object that could receive errors. It 
# is only valid when path is a directory and options contained IGNORE_ERRORS
# and RECURSIVE.
# @see shutil.rmtree() 
def remove(path, options=option_t.NONE, on_error=None):
	path_string = unicode(path)
	
	if is_directory(path_string):
		if options & option_t.RECURSIVE:
			if options & option_t.IGNORE_ERRORS:
				shutil.rmtree(path_string, True, on_error)
			else:				
				shutil.rmtree(path_string, False, on_error)
		else:
			os.rmdir(path_string)
	else:
		os.remove(path_string)
	
def current_path():
	return os.getcwdu();

def file_size(path):
	return os.path.getsize(path) 

def exists(path):
	return os.path.exists(unicode(path))		

def equivalent(path1, path2):
	path1 = unicode(path1)
	path2 = unicode(path2)
	
	if is_symbolic_link(path1):
		path1 = read_symbolic_link(path1)
		
	if is_symbolic_link(path2):
		path2 = read_symbolic_link(path2)
		
	return os.path.realpath(path1) == os.path.realpath(path2)

# Override os.path.samefile, it have not be supported in win32 with python 2.x.
if ( sys.version_info.major <= 2 ) and ( sys.platform == 'win32' ):
	if not hasattr(os.path, 'samefile'):
		os.path.samefile = equivalent
		
def is_directory(path):
	return os.path.isdir(unicode(path))

## Check if a path is a regular file .
# 
# @param path: The path we want to take a check
# @note The hard link is also a regular file !
def is_regular_file(path):
	return os.path.isfile(unicode(path))

def is_symbolic_link(path):
	return os.path.islink(unicode(path))
	
def is_other(path):
	return ( 
		exists(path) 
		and (not is_regular_file(path))
		and (not is_directory(path)) 
		and (not is_symbolic_link(path)) 
		)

def rename(old_path, new_path):
	os.rename(old_path, new_path)
		


