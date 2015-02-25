# -*- coding: UTF-8 -*-



import sys

if sys.platform == "win32":
	from .win32 import Mouse
else:
	from .xdotool import Mouse

