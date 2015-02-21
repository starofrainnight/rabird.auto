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
    
    @classmethod
    def get_title(cls, handle):
        return win32gui.GetWindowText(handle).decode(locale.getpreferredencoding())
    
    
    @classmethod
    def exists(cls, **kwargs):
        return len(cls.find(**kwargs)) > 0
    
    @classmethod
    def find(cls, **kwargs):
        result = super(Window, cls).find(**kwargs)
    
        def enum_window_callback(hwnd, context):
            result, kwargs = context
            
            if "title" in kwargs:
                if re.match(kwargs["title"], cls.get_title(hwnd)) is None:
                    return True
            
            if "id" in kwargs:
                if kwargs["id"] != win32gui.GetDlgCtrlID(hwnd):
                    return True

            result.append(hwnd)
            
            if kwargs["find_count"] > 0:
                if len(result) >= kwargs["find_count"]:
                    return False # Break EnumChildWindows() process 
            
            return True
        
        __enum_windows(kwargs["parent"], enum_window_callback, [result, kwargs])
        
        return result
    
    @classmethod
    def activate(cls, handle):
        win32gui.SetForegroundWindow(handle)    
        
