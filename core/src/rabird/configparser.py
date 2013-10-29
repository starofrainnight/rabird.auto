'''
Created on 2013-5-10

@author: "HongShe Liang <starofrainnight@gmail.com>"
'''

#--IMPORT_ALL_FROM_FUTURE--#

from six.moves import configparser
import rabird.collections
import StringIO 
import io

##
# An advance ConfigParser build on configparser.ConfigParser.
# 
# It's new features:
#  
#    * set() will now automatic create section if there do not have section.
#    * Support ini files that contained unnamed section.
#
class ConfigParser(configparser.ConfigParser):
	def __init__(self, *args, **kwargs): 
		if (sys.version_info[0] <= 2) and (sys.version_info[1] <= 6):
			# Fixed python 2.6.x dict_type not equal to OrderedDict
			if (len(args) < 2) and ('dict_type' not in kwargs):
				kwargs['dict_type'] = rabird.collections.OrderedDict
				
		if issubclass(ConfigParser, object):
			super(ConfigParser, self).__init__(*args, **kwargs)
		else:
			configparser.ConfigParser.__init__(self, *args, **kwargs)
			
		self.UNNAMED_SECTION = '#--ConfigParser--INTERNAL--DEFAULT-SECTION--#'
		
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
		
		while True:
			line = fp.readline()
			if len(line) <= 0:
				break
				
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
		abuffer = abuffer[len(string_io.readline()):]
		fileobject.write(abuffer)		
		
			