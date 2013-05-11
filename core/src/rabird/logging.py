'''
Created on 2013-5-9

@author: HongShe Liang <starofrainnight@gmail.com>
'''

import sys
import os

# Import the global logging unit, not our logging .
global_logging = __import__('logging')

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
			
	# Set default level to logging.INFO .
	if 'level' not in arguments.keys():
		arguments['level'] = global_logging.INFO
		
	global_logging.basicConfig(**arguments)
	
	# Added console handler only there have filename argument. 
	if 'filename' in arguments.keys():
		global_logging.getLogger().addHandler(global_logging.StreamHandler(sys.stdout))
		
		