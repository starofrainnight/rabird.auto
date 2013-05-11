'''
Created on 2013-5-10

@author: "HongShe Liang <starofrainnight@gmail.com>"
'''

#--IMPORT_ALL_FROM_FUTURE--#

from six.moves import configparser

class config_parser_t(configparser.ConfigParser):
	def set(self, section, option, value):
		if not self.has_section(section):
			self.add_section(section)
		
		super(config_parser_t, self).set(section, option, str(value))