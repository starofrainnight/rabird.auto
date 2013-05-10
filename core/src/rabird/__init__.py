
#--IMPORT_ALL_FROM_FUTURE--#

__import__('pkg_resources').declare_namespace(__name__)

import sys
from . import version

version_info = version.version_info
__version__ = version.__version__

if sys.platform == 'win32' :
	from . import windows_api
	from . import windows_fix	

def monkey_patch():
	if sys.platform == 'win32' :
		if sys.version_info.major <= 2 :
			windows_fix.monkey_patch()
			
