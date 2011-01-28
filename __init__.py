import sys

if sys.platform == "win32" :
	if sys.version_info.major <= 2 :
		import rabird_windows_fix
	
	import rabird_windows_api as windows_api
