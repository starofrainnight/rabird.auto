
#--IMPORT_ALL_FROM_FUTURE--#

from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.remote.command import Command 
from . import webelement 

def monkey_patch():
    WebElement.set_attribute = webelement.set_attribute
    WebElement.find_elements_by_attr = webelement.find_elements_by_attr
    WebElement.wait_element = webelement.wait_element    
    WebElement.force_focus = webelement.force_focus    
    WebElement.force_click = webelement.force_click
    