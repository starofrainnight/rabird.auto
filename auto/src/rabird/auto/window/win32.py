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
    
    @property
    def class_name(self):
        text = win32gui.GetClassName(self.__handle)
        return text.decode(locale.getpreferredencoding())
    
    @property
    def geometry(self):
        # FIXME : While the window minimized, here return a wrong
        # result. 
        result = win32gui.GetWindowRect(self.__handle)
        return (result[0], result[1], result[2] - result[0], result[3] - result[1])
    
    def raise_(self):
        win32gui.SetForegroundWindow(self.__handle)
        
    def activate(self):
        win32gui.SetForegroundWindow(self.__handle)
        
    def close(self):
        win32gui.CloseWindow(self.__handle)
        
class Manager(common.Manager):
    
    def __init__(self):
        super(Manager, self).__init__()
    
    @property
    def active_window(self):
        return Window(win32gui.GetActiveWindow())
    
    def find(self, **kwargs):
        self._prepare_find_arguments(kwargs)
        
        result = []
    
        def enum_window_callback(hwnd, context):
            result, kwargs = context
            window = Window(hwnd)
            
            if "title" in kwargs:
                if re.match(str(kwargs["title"]), window.title) is None:
                    return True
            
            if "win32_control_id" in kwargs:
                if int(kwargs["win32_control_id"]) != win32gui.GetDlgCtrlID(hwnd):
                    return True
                
            if "class_name" in kwargs:
                if re.match(str(kwargs["class_name"]), window.class_name) is None:
                    return True 

            result.append(window)
            
            if kwargs["limit"] > 0:
                if len(result) >= kwargs["limit"]:
                    return False # Break EnumChildWindows() process 
            
            return True
        
        __enum_windows(kwargs["parent"], enum_window_callback, [result, kwargs])
        
        return result
    
        
