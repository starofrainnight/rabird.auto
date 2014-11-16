
#--IMPORT_ALL_FROM_FUTURE--#

# Import the global selenium unit, not our selenium .
global_selenium = __import__('selenium')
import types
import time
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.remote.command import Command 

def execute_script(self, script, *args):
    """
    Synchronously Executes JavaScript in the current window/frame.

    :Args:
     - script: The JavaScript to execute.
     - \*args: Any applicable arguments for your JavaScript.

    :Usage:
        driver.execute_script('document.title')
    """
    converted_args = list(args)
    return self._parent.execute(Command.EXECUTE_SCRIPT,
        {'script': script, 'args':converted_args})['value']
        
def set_attribute(self, name, value):
    script = "arguments[0].setAttribute('%s', '%s')"  % (name, value)
    self._execute_script(script)
        
def find_elements_by_attr(self, context, attributes, max_count=-1):
    """
    Fixed find_elements() of webelement that could not find multiply-class controls
    
    Invalid even methods that provided below references:
    
    http://stackoverflow.com/questions/15699900/compound-class-names-are-not-supported-error-in-webdriver
    http://stackoverflow.com/questions/10658907/selenium-python-find-element-by-class-name-stopped-working-from-v-2-2-to-2-21
    
    @arg context tag name or elements
    """
    
    result = []
    
    if isinstance(context, str) or isinstance(context, unicode):
        elements = self.find_elements_by_tag_name(context)
    else:
        elements = context
        
    for element in elements:
        is_matched = True
        for k, v in attributes.iteritems():
            if element.get_attribute(k) != v:
                is_matched = False
                break
                
        if not is_matched:
            continue
            
        result.append(element)
        if (max_count > 0) and (len(result) >= max_count):
            break
            
    return result
    
def wait_element(self, context, attributes, timeout=30):
    """
    @arg timeout -1 means infinite
    """
    
    result = []
    while True:
        print('Waitting element : %s.' % (str(attributes)))
        
        element = self.find_elements_by_attr(context, attributes, 1)
        if element is not None:
            return element
            
        time.sleep(1)
        if timeout > 0:
            timeout -= 1
            if timeout <= 0:
                break
        
    return None

def force_focus(self):
    global_selenium.webdriver.ActionChains(self._parent).move_to_element(self).perform()

def force_click(self):
    global_selenium.webdriver.ActionChains(self._parent).move_to_element(self).click(self).perform()
        
def monkey_patch():
    WebElement._execute_script = execute_script
    WebElement.set_attribute = set_attribute
    WebElement.find_elements_by_attr = find_elements_by_attr
    WebElement.wait_element = wait_element    
    WebElement.force_focus = force_focus    
    WebElement.force_click = force_click
