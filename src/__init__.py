
#--IMPORT_ALL_FROM_FUTURE--#

version_info = (0, 0, 0, 42)
__version__ = ".".join(map(str, version_info))

try:
	import sys
	import os
	import io
	import threading
	import atexit 
	import types # for all standard type values for buildin type()
	import time

	from . import mouse
	from . import system
	from . import compatible
	
	if sys.platform == "win32" :
		import win32console 
		import win32api
		import win32file
		from . import windows_api
		from . import windows_fix	
	
	def monkey_patch():
		if sys.platform == "win32" :
			if sys.version_info.major <= 2 :
				windows_fix.monkey_patch()
except ImportError as e:
	# This is to make Debian packaging easier, it ignores import
	# errors of greenlet so that the packager can still at least
	# access the version.  Also this makes easy_install a little quieter
	if 'rabird' not in str(e):
		# any other exception should be printed
		import traceback
		traceback.print_exc()
		

