'''
Created on 2013-5-10

@author: "HongShe Liang <starofrainnight@gmail.com>"
'''

#--IMPORT_ALL_FROM_FUTURE--#

from six.moves import configparser
from . import collections
import StringIO 
import io
import os
import re

##
# An advance ConfigParser build on configparser.ConfigParser.
# 
# Features:
#  
#  * set() will automatic create section if there do not have section.
#  * Support ini files that contained unnamed section.
#  * Default to case sensitive, actually most ini files are case sensitive, 
#    if you want case insensitive, just set like below:
#        object.optionxform = rabird.ConfigParser.optionxform
#  * Removed spaces around '=', some ini parser do not accept the spaces 
#    around '='.
#  * Support comments start with '#', ';'
#  * Support empty lines
#
class ConfigParser(configparser.ConfigParser):
	UNNAMED_SECTION = '#--ConfigParser--INTERNAL--UNNAMED-SECTION--#'
	# It will transfer to empty line
	__EMPTY_OPTION = '--ConfigParser--INTERNAL--EMPTY-SECTION--'
	# It will transfer to comment line
	__COMMENT_OPTION = '--ConfigParser--INTERNAL--COMMENT-SECTION--'

	def __init__(self, *args, **kwargs): 
		if (sys.version_info[0] <= 2) and (sys.version_info[1] <= 6):
			# Fixed python 2.6.x dict_type not equal to OrderedDict
			if (len(args) < 2) and ('dict_type' not in kwargs):
				kwargs['dict_type'] = collections.OrderedDict
				
		if issubclass(ConfigParser, object):
			super(ConfigParser, self).__init__(*args, **kwargs)
		else:
			configparser.ConfigParser.__init__(self, *args, **kwargs)
			
		# Default to case sensitive
		self.optionxform = str
		
	def set(self, section, option, value):
		if not self.has_section(section):
			self.add_section(section)
		
		# In 3.x, the ConfigParser is a newstyle object
		if issubclass(ConfigParser, object):
			super(ConfigParser, self).set(section, option, str(value))
		else:
			configparser.ConfigParser.set(self, section, option, str(value))
			
	def readfp(self, fp, *args, **kwargs):
		#if hasattr(fp, 'name'):
		# We could only use the readline() by definitions
		abuffer = '[' + self.UNNAMED_SECTION +']' + os.linesep
		
		i = 0
		while True:
			line = fp.readline()
			if len(line) <= 0:
				break
				
			temp_line = line.strip()
			if len(temp_line) <= 0:
				line =  self.__EMPTY_OPTION + str(i) + '=#' + os.linesep
			elif temp_line.startswith('#') or temp_line.startswith(';'):
				line =  self.__COMMENT_OPTION + str(i) + '=#' + line
			abuffer += line
			
		# In 3.x, the ConfigParser is a newstyle object
		fp = StringIO.StringIO(abuffer)
		if issubclass(ConfigParser, object):
			super(ConfigParser, self).readfp(fp, *args, **kwargs)
		else:
			configparser.ConfigParser.readfp(self, fp, *args, **kwargs)
			
	def write(self, fileobject):
		string_io = StringIO.StringIO()
		
		# In 3.x, the ConfigParser is a newstyle object
		if issubclass(ConfigParser, object):
			super(ConfigParser, self).write(string_io)
		else:
			configparser.ConfigParser.write(self, string_io)
		
		abuffer = string_io.getvalue()
		string_io = StringIO.StringIO(abuffer)
		# Remove unused UNNAMED section line. 
		abuffer = abuffer[len(string_io.readline()):]
		
		# Rebuild the string io and strip spaces before and after '=' ( Avoid
		# error happends to some strict ini format parsers )
		string_io = StringIO.StringIO(abuffer)
		
		abuffer = ''
		regexp = re.compile(r'([^\[][^=]*)=(.*)')
		while True:
			line = string_io.readline()
			if len(line) <= 0:
				break
			
			m = regexp.match(line)
			if m is not None:
				if m.group(1).startswith(self.__EMPTY_OPTION):
					# Emtpty line
					pass
				elif m.group(1).startswith(self.__COMMENT_OPTION):
					# Remove the prefix ' #', the rest is comments !
					abuffer += m.group(2)[2:] + os.linesep
				else:					
					abuffer += '%s=%s%s' % (m.group(1).strip(), m.group(2).strip(), os.linesep) 
			else:
				abuffer += line
		
		fileobject.write(abuffer)		
		
			