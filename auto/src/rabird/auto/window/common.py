'''
@date 2015-02-21
@author Hong-She Liang <starofrainnight@gmail.com>
'''

import time

__options = dict()

class Window(object):
    @classmethod
    def find(cls, **kwargs):
        if "find_count" not in kwargs:
            kwargs["find_count"] = 1
            
        if "parent" not in kwargs:
            kwargs["parent"] = None
            
        return []
    
    @classmethod
    def exists(cls, **kwargs):
        return len(cls.find(**kwargs)) > 0
    
    @classmethod
    def wait(cls, timeout=-1.0, **kwargs):
        sleep_interval = 0.1 # 100ms wake up a time. 
        counter = 0.0    
        handles = []
        while True:
            handles = cls.find(**kwargs)
            if (len(handles) <= 0) and (timeout > 0.0) and (counter > timeout):
                time.sleep(sleep_interval)
                counter += sleep_interval
            else:
                break
            
        return handles    

def set_option(option_name, option_value):
    global __options
    
    if option_name not in __options:
        raise KeyError()
        
    __options[option_name] = option_value
    
    
def get_option(option_name):
    global __options
    
    if option_name not in __options:
        raise KeyError()
        
    return __options[option_name]