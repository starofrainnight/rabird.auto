# -*- coding: UTF-8 -*-

## A module unified all file system related stuffs. 
# 
# @date: 2011-11-13
# @author: starofrainnight

import rabird.compatible
import os

class option_t(object):
	NONE = 0
	
	## If we remove directories recursive ? Only effect
	# on directory remove operation.
	RECURSIVE = 1
	
	# Unused
	FORCE = 2
	
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
		self.__path = os.path.join(self.__path, unicode(rhs))
		return self 
				
	def clear(self):
		self.__path = u""
		
def change_current_path(path):
	os.chdir(str(path))
		
def create_directories(path):
	os.makedirs(str(path))
	
def create_directory(path):
	os.mkdir(str(path))

## Create a hard link ( unimplemented )
def create_hard_link(from_path, to_hard_link_path):
	#os.link(str(from_path), str(to_hard_link_path))
	pass

## Create a symbol link ( unimplemented )
def create_symbol_link(from_path, to_symbol_link_path):
	#os.symlink(str(from_path), str(to_symbol_link_path))
	pass

def copy(from_path, to_path):
	pass

## Remove target path 
#
# @param [in] path: Target path we need to remove
# @param [in] options: A series options to control the remove behaviors.
# @see option_t.
def remove(path, options=option_t.NONE):
	path_string = str(path)
	
	if is_directory(path_string):
		if options & option_t.RECURSIVE:
			os.removedirs(path_string)
		else:
			os.rmdir(path_string)
	else:
		os.remove(path_string)
	
def current_path():
	return os.getcwdu();

def file_size(path):
	return os.path.getsize(path) 

def exists(path):
	return os.path.exists(str(path))		

def is_directory(path):
	return os.path.isdir(str(path))

def is_regular_file(path):
	return os.path.isfile(str(path))

def is_symlink(path):
	return os.path.islink(str(path))

def is_other(path):
	return ( 
		exists(path) 
		and (not is_regular_file(path))
		and (not is_directory(path)) 
		and (not is_symlink(path)) 
		)

		

		


