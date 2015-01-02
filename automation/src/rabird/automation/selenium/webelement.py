
#--IMPORT_ALL_FROM_FUTURE--#

'''
@date 2014-11-16
@author Hong-she Liang <starofrainnight@gmail.com>
'''

import types
import time
import functools
from . import exceptions
from . import utilities
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webdriver import WebDriver

def _execute_with_switch_frame(self, function):
    if  (hasattr(self, '_parent_frame_path') and 
        (len(self._parent_frame_path) > 0)):
        self._parent.switch_to_default_content()
        try:
            self._parent.switch_to_frame(self._parent_frame_path)
            result = function()
        finally:
            self._parent.switch_to_default_content()
    else:
        result = function()
    return result

def set_attribute(self, name, value):
    value = utilities.js_string_encode(value)
    script = "arguments[0].setAttribute('%s', '%s');"  % (name, value)
    function = functools.partial(self._parent.execute_script, 
                                 script, self)
    return _execute_with_switch_frame(self, function)

def wait_element_by_xpath(self, xpath, for_appear=True, timeout=-1):
    return wait_element(self, By.XPATH, xpath, for_appear, timeout)

def wait_element_by_css_selector(self, css_selector, for_appear=True, timeout=-1):
    return wait_element(self, By.CSS_SELECTOR, css_selector, for_appear, timeout)
    
def wait_element(self, by, value, for_appear=True, timeout=-1):
    """
    Wait until the element appear or disappear.
    
    @param timeout: If timeout equal to < 0, it will loop infinite. Otherwise 
    it will loop for timeout seconds and raise a NoSuchElementException 
    exception if can not found any element! 
    """
    
    elapsed_time = 0
    element = None
    last_exception = None
    while True:        
        try:
            element = self.find_element(by=by, value=value)
            if for_appear:
                break
        except exceptions.NoSuchElementException as e:
            last_exception = e
            if not for_appear:
                break
        
        time.sleep(1)
        
        # Check if timeout
        if timeout < 0:
            # Loop for infinite
            continue
        
        elapsed_time += 1
        if elapsed_time < timeout:
            raise last_exception
        
        break
    
    return element

def force_focus(self):
    function = functools.partial(self._parent.execute_script, 
                                 "arguments[0].focus();", self)
    _execute_with_switch_frame(self, function)

def force_click(self):
    function = functools.partial(self._parent.execute_script, 
                                 "arguments[0].click();", self)
    _execute_with_switch_frame(self, function)

def _execute(self, command, params=None):
    function = functools.partial(self._old_execute, command, params)
    return _execute_with_switch_frame(self, function)

def find_element(self, by=By.ID, value=None, parent_frame_path=[]):
    if isinstance(self, WebDriver):
        driver = self
    else:
        driver = self._parent
        
        # If "self" is an element and parent_frame_path do not have any 
        # elements, we should inhert the frame path from "self".
        if hasattr(self, "_parent_frame_path") and (len(parent_frame_path) <= 0):
            parent_frame_path = self._parent_frame_path
        
    last_exception = None
    try:
        founded_element = self._old_find_element(by, value)
        founded_element._parent_frame_path = parent_frame_path
        return founded_element        
    except exceptions.NoSuchElementException as e:
        if not driver.is_find_element_recursively:
            raise e
        last_exception = e
        
    # You must invoke self's old find elements method, so that it could search
    # in the element not spread all over the whole HTML.
    elements = self._old_find_elements(By.TAG_NAME, 'iframe')
    if len(elements) <= 0:
        raise last_exception
    
    try:
        for element in elements:
            temporary_frame_path = parent_frame_path + [element]
            driver.switch_to_default_content()
            driver.switch_to_frame(temporary_frame_path)
            try:
                # Here must use driver to find elements, because now it already
                # switched into the frame, so we need to search the whole frame
                # area.
                found_element = driver.find_element(by, value, temporary_frame_path)
                # Avoid stay in the specific frame after last find_element().
                return found_element
            except exceptions.NoSuchElementException as e:
                last_exception = e
    finally:
        driver.switch_to_default_content()
            
    # Can't find any element, we raise the last exception.
    raise last_exception

def find_elements(self, by=By.ID, value=None, parent_frame_path=[]):
    if isinstance(self, WebDriver):
        driver = self
    else:
        driver = self._parent
        
        # If "self" is an element and parent_frame_path do not have any 
        # elements, we should inhert the frame path from "self".
        if hasattr(self, "_parent_frame_path") and (len(parent_frame_path) <= 0):
            parent_frame_path = self._parent_frame_path
        
    founded_elements = self._old_find_elements(by, value)
    for element in founded_elements:
        element._parent_frame_path = parent_frame_path
    
    if not driver.is_find_element_recursively:
        return founded_elements
        
    # You must invoke old find method, do not try to invoke something
    # like find_elements_by_xxx()! There will lead function be invoke 
    # recursively infinite.
    
    # You must invoke self's old find elements method, so that it could search
    # in the element not spread all over the whole HTML.
    elements = self._old_find_elements(By.TAG_NAME, 'iframe')
    if len(elements) <= 0:
        return founded_elements
    
    for element in elements:
        temporary_frame_path = parent_frame_path + [element]
        driver.switch_to_default_content()
        driver.switch_to_frame(temporary_frame_path)
        # Here must use driver to find elements, because now it already
        # switched into the frame, so we need to search the whole frame
        # area.
        founded_elements += driver.find_elements(by, value, temporary_frame_path)
    driver.switch_to_default_content()
    
    return founded_elements
    
