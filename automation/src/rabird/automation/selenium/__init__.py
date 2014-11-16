
#--IMPORT_ALL_FROM_FUTURE--#

from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.remote.command import Command 
from selenium.webdriver.remote.webdriver import WebDriver
from . import webelement 

def monkey_patch():
    WebElement.set_attribute = webelement.set_attribute
    WebElement.force_focus = webelement.force_focus    
    WebElement.force_click = webelement.force_click
    