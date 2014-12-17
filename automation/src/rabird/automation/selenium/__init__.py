
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

    WebDriver._old_switch_to_frame = WebDriver.switch_to_frame
    WebDriver.switch_to_frame = types.MethodType(webdriver.switch_to_frame, None, WebDriver)
    
    WebDriver.wait_element = types.MethodType(webelement.wait_element, None, WebDriver)
    
    