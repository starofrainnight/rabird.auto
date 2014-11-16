
#--IMPORT_ALL_FROM_FUTURE--#

'''
@date 2014-11-16
@author Hong-she Liang <starofrainnight@gmail.com>
'''

# Import the global selenium unit, not our selenium .
global_selenium = __import__('selenium')
import types
import time

def set_attribute(self, name, value):
    value = value.replace(r"'", r"\'") # Replace all r"'" with r"\'"
    value = value.replace("\n", r"\n") 
    value = value.replace("\r", r"\r")
    value = value.replace("\t", r"\t")  
    script = "arguments[0].setAttribute('%s', '%s')"  % (name, value)
    self._parent.execute_script(script, self)
        
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
        