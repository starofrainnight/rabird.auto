
#--IMPORT_ALL_FROM_FUTURE--#

__import__('pkg_resources').declare_namespace(__name__)

import sys

version_info = (0, 0, 2)
__version__ = '.'.join(map(str, version_info))
__monkey_patched = False

try:
	import rabird
	
	if sys.platform == 'win32' :
		from . import windows_api
		from . import windows_fix
	
	# Known Issues : Can't work with eventlet, Why?
	def monkey_patch():
		global __monkey_patched
		
		# During setup process, the ez_setup.py will load the rabird library
		# already existed in python library. So we need to check the patched
		# information to determine if we need to do again. 
		existed_monkey_patched = rabird.__monkey_patched
		if __monkey_patched or existed_monkey_patched:
			return
			
		if sys.platform == 'win32' :
			if sys.version_info[0] <= 2 :
				windows_fix.monkey_patch()
				
		__monkey_patched = True
		
except ImportError as e:
	if 'rabird' not in str(e):
		# any other exception should be printed
		import traceback
		traceback.print_exc()