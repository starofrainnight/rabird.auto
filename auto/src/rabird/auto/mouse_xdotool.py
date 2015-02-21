'''
@date 2015-02-21
@author Hong-She Liang <starofrainnight@gmail.com>
'''

import os
import re
import subprocess
from .mouse_constant import *

class Mouse(object):
    ## return current mouse absolute position
    @classmethod
    def position(cls):
        p = subprocess.Popen(["xdotool", "getmouselocation"], stdout=subprocess.PIPE)
        output = p.communicate()[0]
        matched = re.match(".*x:(\d+)\s*y:(\d+)\s*.*", output)
        return [int(matched.group(1)), int(matched.group(2))]
    
    @classmethod
    def move(cls, position):
        os.system("xdotool mousemove --sync %s %s" % (int(position[0]), int(position[1])))
    
    ##  
    @classmethod
    def button_up(cls, button_type = ButtonType.LEFT ):
        if ButtonType.LEFT == button_type:
            os.system("xdotool mouseup 1") 
        elif ButtonType.RIGHT == button_type:
            os.system("xdotool mouseup 3")
        elif ButtonType.MIDDLE == button_type:
            os.system("xdotool mouseup 2")
            
    @classmethod
    def button_down(cls, button_type = ButtonType.LEFT ):
        if ButtonType.LEFT == button_type:
            os.system("xdotool mousedown 1")
        elif ButtonType.RIGHT == button_type:
            os.system("xdotool mousedown 3")
        elif ButtonType.MIDDLE == button_type:
            os.system("xdotool mousedown 2")
            
            