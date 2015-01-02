
#--IMPORT_ALL_FROM_FUTURE--#

from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.remote.command import Command 
from selenium.webdriver.remote.webdriver import WebDriver
from . import webelement
from . import webdriver 
import types

__is_monkey_patched = False

def monkey_patch():
    global __is_monkey_patched
    
    if __is_monkey_patched:
        return

    __is_monkey_patched = True
        
    WebElement.set_attribute = types.MethodType(webelement.set_attribute, None, WebElement) 
    WebElement.force_focus = types.MethodType(webelement.force_focus, None, WebElement)    
    WebElement.force_click = types.MethodType(webelement.force_click, None, WebElement)
    WebElement.wait_element = types.MethodType(webelement.wait_element, None, WebElement)
    
    WebElement._old_execute = WebElement._execute 
    WebElement._execute = types.MethodType(webelement._execute, None, WebElement)

    WebElement._old_find_element = WebElement.find_element
    WebElement.find_element = types.MethodType(webelement.find_element, None, WebElement)
    
    WebElement._old_find_elements = WebElement.find_elements
    WebElement.find_elements = types.MethodType(webelement.find_elements, None, WebElement)
    
    WebElement.wait_element_by_css_selector = types.MethodType(webelement.wait_element_by_css_selector, None, WebElement)
    WebDriver.wait_element_by_css_selector = types.MethodType(webelement.wait_element_by_css_selector, None, WebDriver)

    WebElement.wait_element_by_xpath = types.MethodType(webelement.wait_element_by_xpath, None, WebElement)
    WebDriver.wait_element_by_xpath = types.MethodType(webelement.wait_element_by_xpath, None, WebDriver)

    WebDriver._old_switch_to_frame = WebDriver.switch_to_frame
    WebDriver.switch_to_frame = types.MethodType(webdriver.switch_to_frame, None, WebDriver)
    
    WebDriver._old_find_element = WebDriver.find_element
    WebDriver.find_element = types.MethodType(webelement.find_element, None, WebDriver)
    
    WebDriver._old_find_elements = WebDriver.find_elements
    WebDriver.find_elements = types.MethodType(webelement.find_elements, None, WebDriver)
    
    WebDriver.wait_element = types.MethodType(webelement.wait_element, None, WebDriver)
    WebDriver.is_find_element_recursively = False
    
