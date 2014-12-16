
#--IMPORT_ALL_FROM_FUTURE--#

from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.remote.command import Command 
from selenium.webdriver.remote.webdriver import WebDriver
from . import webelement 
import types

def monkey_patch():
    WebElement.set_attribute = types.MethodType(webelement.set_attribute, None, WebElement) 
    WebElement.force_focus = types.MethodType(webelement.force_focus, None, WebElement)    
    WebElement.force_click = types.MethodType(webelement.force_click, None, WebElement)
    WebElement.wait_element = types.MethodType(webelement.wait_element, None, WebElement)
    WebDriver.wait_element = types.MethodType(webelement.wait_element, None, WebDriver)
    