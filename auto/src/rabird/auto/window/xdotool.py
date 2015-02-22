'''
@date 2015-02-22
@author Hong-She Liang <starofrainnight@gmail.com>
'''

import re
import subprocess
from . import common
from ..mouse import Mouse

class Window(common.Window):
    def __init__(self, handle):
        super(Window, self).__init__()
        
        self.__handle = int(handle)
        
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
        self.__mouse = Mouse()
    
    def get_active(self):
        output = subprocess.check_output(["xdotool", "getactivewindow"])
        return Window(int(output.strip('\r\n').strip()))
    
    def get_from_position(self, position):
        old_position = None
        
        if position != self.__mouse.position():
            old_position = self.__mouse.position()
            self.__mouse.move(position)
        try:
            output = subprocess.check_output(["xdotool", "getmouselocation"])
            matched = re.match("(?:\n|.)*window:(\d+)*(?:\n|.)*", output)
            return Window(int(matched.group(1)))
        finally:
            if old_position is not None:
                self.__mouse.move(old_position)        
    
    def find(self, **kwargs):
        self._prepare_find_arguments(kwargs)
        
        result = []
        
        command = ["xdotool", "search"]
        command.append("--all")
        command.append("--sync")
        
        if ("class_name" in kwargs) and ("title" in kwargs):
            # Seems xdotool can't work if class name and title 
            # at the sametime. So we search by ourself.
            command += ["--classname", str(kwargs["class_name"])]
            
            output = subprocess.check_output(command)
            window_ids = re.findall("\d+", output, re.M)
            window_ids = [int(window_id) for window_id in window_ids]
            
            for window_id in window_ids:
                window = Window(window_id)
                if re.match(str(kwargs["title"]), window.title) is None:
                    continue
    
                result.append(window)
                
                if kwargs["limit"] > 0:
                    if len(result) >= kwargs["limit"]:
                        break 
        else:
            if kwargs["limit"] > 0:
                command += ["--limit", str(kwargs["limit"])]

            if "title" in kwargs:
                command += ["--name", str(kwargs["title"])]
                
            if "class_name" in kwargs:
                command += ["--classname", str(kwargs["class_name"])]
            
            output = subprocess.check_output(command)
            window_ids = re.findall("\d+", output, re.M)
            result += [Window(int(window_id)) for window_id in window_ids] 
        
        return result
    