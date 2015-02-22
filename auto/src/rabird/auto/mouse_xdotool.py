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
        output = subprocess.check_output(["xdotool", "getmouselocation"])
        matched = re.match(".*x:(\d+)\s*y:(\d+)\s*.*", output)
        return [int(matched.group(1)), int(matched.group(2))]
    
    @classmethod
    def move(cls, position):
        subprocess.call(["xdotool", "mousemove", "--sync", position[0], position[1]])
    
    ##  
    @classmethod
    def button_up(cls, button_type = ButtonType.LEFT ):
        if ButtonType.LEFT == button_type:
            subprocess.call(["xdotool", "mouseup", "1"]) 
        elif ButtonType.RIGHT == button_type:
            subprocess.call(["xdotool", "mouseup", "3"])
        elif ButtonType.MIDDLE == button_type:
            subprocess.call(["xdotool", "mouseup", "2"])
            
    @classmethod
    def button_down(cls, button_type = ButtonType.LEFT ):
        if ButtonType.LEFT == button_type:
            subprocess.call(["xdotool", "mousedown", "1"])
        elif ButtonType.RIGHT == button_type:
            subprocess.call(["xdotool", "mousedown", "3"])
        elif ButtonType.MIDDLE == button_type:
            subprocess.call(["xdotool", "mousedown", "2"])
            
            