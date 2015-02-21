'''
@date 2015-02-21
@author Hong-She Liang <starofrainnight@gmail.com>
'''


class FindContext(object):
    pass

__options = dict()

class Window(object):
    pass

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