'''
Created on 2013-5-10

@author: "HongShe Liang <starofrainnight@gmail.com>"
'''

#--IMPORT_ALL_FROM_FUTURE--#

from six.moves import configparser

class ConfigParser(configparser.ConfigParser):
	def set(self, section, option, value):
		if not self.has_section(section):
			self.add_section(section)
		
		# In 3.x, the ConfigParser is a newstyle object
		if issubclass(ConfigParser, object):
			super(ConfigParser, self).set(section, option, str(value))
		else:
			configparser.ConfigParser.set(self, section, option, str(value))
			