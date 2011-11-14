# -*- coding: UTF-8 -*-

## A module unified all file system related stuffs. 
# 
# @date 2011-11-13
# @author: starofrainnight

import rabird.compatible

class path_t(rabird.compatible.unicode_t):
	def __init__(self, path=u"" ):
		super(path_t, self).__init__(self)
		
		## Internal path string, must be in unicode format.
		self.__path = unicode(path)
	
	def __unicode__(self):
		return self.__path



