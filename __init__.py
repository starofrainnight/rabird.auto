import sys

if sys.platform == "win32" :
	if sys.version_info.major <= 2 :
		from . import windows_fix
	
	from . import windows_api
	
from . import automatization
