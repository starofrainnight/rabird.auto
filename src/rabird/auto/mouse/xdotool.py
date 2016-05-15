'''
@date 2015-02-21
@author Hong-She Liang <starofrainnight@gmail.com>
'''

import os
import re
import sys
import six
import subprocess
from . import common

def _check_output(*args, **kwargs):
    output = subprocess.check_output(*args, **kwargs)
    if six.PY3:
        output = output.decode(sys.getdefaultencoding())
    return output 

class Mouse(common.Mouse):
    def __init__(self):
        super(Mouse, self).__init__()
        
    ## return current mouse absolute position
    def position(self):
        output = _check_output(["xdotool", "getmouselocation"])
        matched = re.match(".*x:(\d+)\s*y:(\d+)\s*.*", output)
        return [int(matched.group(1)), int(matched.group(2))]
    
    def move(self, position):
        subprocess.call(["xdotool", "mousemove", "--sync", str(position[0]), str(position[1])])
    
    def button_up(self, button_type = common.ButtonType.LEFT ):
        if common.ButtonType.LEFT == button_type:
            subprocess.call(["xdotool", "mouseup", "1"]) 
        elif common.ButtonType.RIGHT == button_type:
            subprocess.call(["xdotool", "mouseup", "3"])
        elif common.ButtonType.MIDDLE == button_type:
            subprocess.call(["xdotool", "mouseup", "2"])
            
    def button_down(self, button_type = common.ButtonType.LEFT ):
        if common.ButtonType.LEFT == button_type:
            subprocess.call(["xdotool", "mousedown", "1"])
        elif common.ButtonType.RIGHT == button_type:
            subprocess.call(["xdotool", "mousedown", "3"])
        elif common.ButtonType.MIDDLE == button_type:
            subprocess.call(["xdotool", "mousedown", "2"])
            
            