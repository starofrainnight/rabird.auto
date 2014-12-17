
#--IMPORT_ALL_FROM_FUTURE--#

'''
@date 2014-11-16
@author Hong-she Liang <starofrainnight@gmail.com>
'''

# Import the global selenium unit, not our selenium .
global_selenium = __import__('selenium')
import types
import time
from . import exceptions
from . import utilities

def set_attribute(self, name, value):
    value = utilities.js_string_encode(value)
    script = "arguments[0].setAttribute('%s', '%s');"  % (name, value)
    self._parent.execute_script(script, self)
    
def wait_element(self, by, value, for_appear=True, timeout=-1):
    elapsed_time = 0
    element = None
    while True:        
        try:
            element = self.find_element(by=by, value=value)
            if for_appear:
                break
        except global_selenium.common.exceptions.NoSuchElementException:
            if not for_appear:
                break
        
        time.sleep(1)
        
        # Check if timeout
        if timeout < 0:
            # Loop for infinite
            continue
        
        elapsed_time += 1
        if elapsed_time < timeout:
            raise exceptions.TimeoutError()
        
        break
    
    return element

def force_focus(self):
    self._parent.execute_script("arguments[0].focus();", self);

def force_click(self):
    self._parent.execute_script("arguments[0].click();", self);

def _execute(self, command, params=None):
    if hasattr(self, '_parent_frame_path'):
        self._parent.switch_to_frame(self._parent_frame_path)
        result = self._old_execute(command, params)
        self._parent.switch_to_default_content()
    else:
        result = self._old_execute(command, params)

    return result
