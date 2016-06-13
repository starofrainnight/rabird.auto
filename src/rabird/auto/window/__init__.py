'''
@date 2013-8-14
@author Hong-She Liang <starofrainnight@gmail.com>
'''

# -*- coding: UTF-8 -*-


import sys

if sys.platform == "win32":
    from .win32 import Manager, Window
else:
    from .xdotool import Manager, Window
