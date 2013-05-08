
#--IMPORT_ALL_FROM_FUTURE--#

import sys
import os
import io
import threading
import atexit 
import types # for all standard type values for buildin type()
import pickle
import time

from . import mouse
from . import system
from . import filesystem
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
	
