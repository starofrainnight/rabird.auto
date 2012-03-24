import sys
import string

def __string_find(s, *args):
	return s.find(*args)

#
# Fixed errors that report by distutils depends by jaraco.windows.filesystem 
# when import rabird library : 
#
# File "D:\sb\python\lib\distutils\util.py", line 43, in get_platform
# AttributeError: 'module' object has no attribute 'find'
#
if not hasattr(string, 'find'):
	string.find = __string_find
		
if sys.platform == "win32" :
	if sys.version_info.major <= 2 :
		import rabird.windows_fix
	
	import rabird.windows_api
	
import rabird.mouse
import rabird.system
import rabird.filesystem
import rabird.compatible
import rabird.string
