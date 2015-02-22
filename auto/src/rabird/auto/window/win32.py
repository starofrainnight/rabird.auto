'''
@date 2015-02-21
@author Hong-She Liang <starofrainnight@gmail.com>
'''

import win32gui
import pywintypes
import time
import locale
import re
from . import common

def __enum_windows(parent, callback, extra):
    try:
        win32gui.EnumChildWindows(parent, callback, extra)
    except pywintypes.error as e:
        if 0== e.winerror:
            # No errors, just function break from EnumChildWindows()
            pass
        elif 2 == e.winerror:
            # No errors, just function break from EnumChildWindows(), in win7 x64
            pass
        else:
            raise e
        
class Window(common.Window):
    def __init__(self, handle):
        super(Window, self).__init__()
        
        self.__handle = handle
        
    @property
    def title(self):
        text = win32gui.GetWindowText(self.__handle)
        return text.decode(locale.getpreferredencoding())    
        
    def raise_(self):
        win32gui.SetForegroundWindow(self.__handle)
        
class Manager(common.Manager):
    
    def __init__(self):
        super(Manager, self).__init__()
    
    def find(self, **kwargs):
        result = super(Manager, self).find(**kwargs)
    
        def enum_window_callback(hwnd, context):
            result, kwargs = context
            window = Window(hwnd)
            
            if "title" in kwargs:
                if re.match(kwargs["title"], window.title) is None:
                    return True
            
            if "id" in kwargs:
                if kwargs["id"] != win32gui.GetDlgCtrlID(hwnd):
                    return True

            result.append(window)
            
            if kwargs["find_count"] > 0:
                if len(result) >= kwargs["find_count"]:
                    return False # Break EnumChildWindows() process 
            
            return True
        
        __enum_windows(kwargs["parent"], enum_window_callback, [result, kwargs])
        
        return result
    
        
