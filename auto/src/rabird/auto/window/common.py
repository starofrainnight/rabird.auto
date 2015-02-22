'''
@date 2015-02-21
@author Hong-She Liang <starofrainnight@gmail.com>
'''

import time

class Window(object):
    def __init__(self):
        pass
    
    def raise_(self):
        '''
        Raise the window to top most .
        '''
        raise NotImplemented()
    
    @property
    def title(self):
        '''
        Get the window's title.
        '''
        raise NotImplemented()

class Manager(object):
    def __init__(self):
        self.__options = dict()
        
    def set_option(self, option_name, option_value):
        if option_name not in self.__options:
            raise KeyError()
            
        self.__options[option_name] = option_value        
        
    def get_option(self, option_name):
        if option_name not in self.__options:
            raise KeyError()
            
        return self.__options[option_name]
    
    def find(self, **kwargs):
        if "find_count" not in kwargs:
            kwargs["find_count"] = 1
            
        if "parent" not in kwargs:
            kwargs["parent"] = None
            
        return []
    
    def exists(self, **kwargs):
        return len(self.find(**kwargs)) > 0
    
    def wait(self, timeout=-1.0, **kwargs):
        sleep_interval = 0.1 # 100ms wake up a time. 
        counter = 0.0    
        handles = []
        while True:
            handles = self.find(**kwargs)
            if (len(handles) <= 0) and (timeout > 0.0) and (counter > timeout):
                time.sleep(sleep_interval)
                counter += sleep_interval
            else:
                break
            
        return handles    

