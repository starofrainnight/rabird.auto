# -*- coding: UTF-8 -*-

#--IMPORT_ALL_FROM_FUTURE--#

import sys

if sys.platform == "win32":
	from .win32 import Mouse
else:
	from .xdotool import Mouse

