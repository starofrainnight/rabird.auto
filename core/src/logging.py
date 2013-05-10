'''
Created on 2013-5-9

@author: Administrator
'''

import os
import logging

def load_basic_config_from_environment():
	arguments = {
		'level':None,
		'filename':None,
		'filemode':None,
		'format':None,
		'datefmt':None,
		'style':None,
	} 
	
	for k in arguments.keys():
		try:
			envionment_text = 'PYTHON_LOGGING_{}'.format(k.upper())
			arguments[k] = os.environ[envionment_text]
		except ValueError:
			pass
		except KeyError:
			pass
			
	# Remove all arguments that is None value.
	keys = list(arguments.keys())
	for k in keys:
		if arguments[k] is None:
			del arguments[k]
			
	return logging.basicConfig(**arguments)
		
		