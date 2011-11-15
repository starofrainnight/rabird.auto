# -*- coding: UTF-8 -*-

## A module unified all file system related stuffs. 
# 
# @date 2011-11-13
# @author starofrainnight

import rabird.compatible
import os

class path_t(rabird.compatible.unicode_t):
	def __init__(self, path=u"" ):
		super(path_t, self).__init__()
		
		## Internal path string, must be in unicode format.
		self.__path = unicode(path)
	
	## Support str(path object) or unicode(path object), they are all return
	# an unicode object, actually rabird library is only support unicode 
	# string!
	def __unicode__(self):
		return self.__path
	
	def __div__(self, rhs):
		self.__path = os.path.join( self.__path, unicode(rhs) )
		return self 
				
	def clear(self):
		self.__path = u""
		
		
def current_path():
	return os.getcwdu();

def exists( path ):
	return os.path.exists( str(path) )		

def is_directory( path ):
	return os.path.isdir( str(path) )

def is_regular_file( path ):
	return os.path.isfile( str(path) )

def is_symlink( path ):
	return os.path.islink( str(path) )

def is_other( path ):
	return ( 
		exists( path ) 
		and ( not is_regular_file( path ) )
		and ( not is_directory( path ) ) 
		and ( not is_symlink( path ) ) 
		)

		


