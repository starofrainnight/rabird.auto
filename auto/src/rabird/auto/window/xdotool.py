'''
@date 2015-02-22
@author Hong-She Liang <starofrainnight@gmail.com>
'''

import re
import subprocess
from . import common

class Window(common.Window):
    def __init__(self, handle):
        super(Window, self).__init__()
        
        self.__handle = handle
        
    @property
    def title(self):
        output = subprocess.check_output(["xdotool", "getwindowname", str(self.__handle)])
        return output.strip('\r\n').strip()
    
    @property
    def geometry(self):
        output = subprocess.check_output(["xdotool", "getwindowgeometry", str(self.__handle)])
        matched = re.match("(?:\n|.)*(\d+),(\d+)(?:\n|.)*(\d+)x(\d+)(?:\n|.)*", output, re.M)
        return (int(matched.group(1)),
            int(matched.group(2)),
            int(matched.group(3)),
            int(matched.group(4)))
    
    def raise_(self):
        subprocess.call(["xdotool", "windowraise", "--sync", str(self.__handle)]) 
        
    def activate(self):
        subprocess.call(["xdotool", "windowactivate", "--sync", str(self.__handle)])
        
    def close(self):
        subprocess.call(["xdotool", "windowkill", "--sync", str(self.__handle)])
        
class Manager(common.Manager):
    
    def __init__(self):
        super(Manager, self).__init__()
    
    @property
    def active_window(self):
        output = subprocess.check_output(["xdotool", "getactivewindow"])
        return Window(int(output.strip('\r\n').strip()))
    
    def find(self, **kwargs):
        result = super(Manager, self).find(**kwargs)
        command = ["xdotool", "search"]
        command.append("--all")
        command.append("--sync")
        
        if "title" in kwargs:
            command += ["--name", str(kwargs["title"])]

        if kwargs["limit"] > 0:
            command += ["--limit", str(kwargs["limit"])]
            
        if "class_name" in kwargs:
            command += ["--classname", str(kwargs["class_name"])]
            
        output = subprocess.call(command)
        window_ids = re.findall("\d+", output, re.M)
        result += [int(window_id) for window_id in window_ids] 
        
        return result