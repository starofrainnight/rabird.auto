from __future__ import unicode_literals
from __future__ import print_function
from __future__ import absolute_import
from __future__ import division
import sys

if sys.platform == "win32" :
	if sys.version_info.major <= 2 :
		import rabird.windows_fix
	
	import rabird.windows_api
	
import rabird.mouse
import rabird.system
import rabird.filesystem
import rabird.compatible
import rabird.string
