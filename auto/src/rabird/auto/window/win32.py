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
    def get_list(cls, parent=None):
        windows = []
        def enum_window_callback(hwnd, windows):
            windows.append(hwnd)
            return True
        
        __enum_windows(parent, enum_window_callback, windows)
        
        return windows
    
    @classmethod
    def exists(cls, **kwargs):
        return (cls.find(**kwargs) is not None)
    
    @classmethod
    def find(cls, title=None, id=None, parent=None):
        result = []
    
        context = common.FindContext()
        context.result = result
        context.title = title
        context.id = id
        
        def enum_window_callback(hwnd, context):
            if context.title is not None:
                if re.match(context.title, cls.get_title(hwnd)) is not None:
                    return True
            
            if context.id is not None:
                if context.id != win32gui.GetDlgCtrlID(hwnd):
                    return True
                
            context.result.append(hwnd)
            
            return False # Break EnumChildWindows() process 
        
        __enum_windows(parent, enum_window_callback, context)
        
        if len(result) > 0:
            return result[0]
        else:
            return None
    
    @classmethod
    def wait(cls, timeout=-1.0, **kwargs):
        sleep_interval = 0.1 # 100ms wake up a time. 
        counter = 0.0    
        handle = None
        while True:
            handle = cls.find(**kwargs)
            if (handle is None) and (timeout > 0.0) and (counter > timeout):
                time.sleep(sleep_interval)
                counter += sleep_interval
            else:
                break
            
        return handle    
    
    @classmethod
    def activate(cls, handle):
        win32gui.SetForegroundWindow(handle)    
        
