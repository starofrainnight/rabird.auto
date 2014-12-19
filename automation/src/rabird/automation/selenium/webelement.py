
#--IMPORT_ALL_FROM_FUTURE--#

'''
@date 2014-11-16
@author Hong-she Liang <starofrainnight@gmail.com>
'''

import types
import time
from . import exceptions
from . import utilities
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webdriver import WebDriver

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
        except exceptions.NoSuchElementException:
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
        self._parent.switch_to_default_content()
        self._parent.switch_to_frame(self._parent_frame_path)
        result = self._old_execute(command, params)
        self._parent.switch_to_default_content()
    else:
        result = self._old_execute(command, params)

    return result

def find_element(self, by=By.ID, value=None, parent_frame_path=[]):
    if isinstance(self, WebDriver):
        driver = self
    else:
        driver = self._parent
        
    last_exception = None
    try:
        founded_element = self._old_find_element(by, value)
        founded_element._parent_frame_path = parent_frame_path
        return founded_element        
    except exceptions.NoSuchElementException as e:
        if not driver.is_find_element_recursively:
            raise e
        last_exception = e
        
    elements = driver._old_find_elements(By.TAG_NAME, 'iframe')
    if len(elements) <= 0:
        raise last_exception
    
    for element in elements:
        temporary_frame_path = parent_frame_path + [element]
        driver.switch_to_default_content()
        driver.switch_to_frame(temporary_frame_path)
        try:
            return self.find_element(by, value, temporary_frame_path)             
        except exceptions.NoSuchElementException as e:
            last_exception = e
            
    # Can't find any element, we raise the last exception.    
    raise last_exception

def find_elements(self, by=By.ID, value=None, parent_frame_path=[]):
    if isinstance(self, WebDriver):
        driver = self
    else:
        driver = self._parent
        
    founded_elements = self._old_find_elements(by, value)
    for element in founded_elements:
        element._parent_frame_path = parent_frame_path
    
    if not driver.is_find_element_recursively:
        return founded_elements
        
    # You must invoke old find method, do not try to invoke something
    # like find_elements_by_xxx()! There will lead function be invoke 
    # recursively infinite.
    elements = driver._old_find_elements(By.TAG_NAME, 'iframe')
    if len(elements) <= 0:
        return founded_elements
    
    for element in elements:
        temporary_frame_path = parent_frame_path + [element]
        driver.switch_to_default_content()
        driver.switch_to_frame(temporary_frame_path)
        founded_elements += self.find_elements(by, value, temporary_frame_path)
    driver.switch_to_default_content()
    
    return founded_elements
    
