
#--IMPORT_ALL_FROM_FUTURE--#

'''
@date 2014-11-16
@author: Hong-she Liang <starofrainnight@gmail.com>
'''

from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException, UnexpectedTagNameException
from . import utilities

class BaseEditor(object):
    def __init__(self, webelement):
        self._element = webelement
    
    @property
    def element(self):
        return self._element
    
    @property
    def text(self):
        raise NotImplementedError()
    
    @text.setter
    def text(self, value):
        raise NotImplementedError()

class Input(BaseEditor):
    def __init__(self, webelement):
        if webelement.tag_name.lower() != "input":
            raise UnexpectedTagNameException("Input only works on <input> "
                                             "elements, not on <%s>" %
                                             webelement.tag_name)
            
        super(Input, self).__init__(webelement)
        
    @property
    def text(self):
#         return self.element.get_attribute("value")
        script = "return arguments[0].value;"
        return self.element._parent.execute_script(script, self.element)
    
    @text.setter
    def text(self, value):
#         self.element.set_attribute("value", value)
        value = utilities.js_string_encode(value)
        script= "return arguments[0].value = '%s';" % value
        self.element._parent.execute_script(script, self.element)
        
class TextArea(BaseEditor):
    def __init__(self, webelement):
        if webelement.tag_name.lower() != "textarea":
            raise UnexpectedTagNameException("TextArea only works on <textarea> "
                                             "elements, not on <%s>" % 
                                             webelement.tag_name)
            
        super(TextArea, self).__init__(webelement)
        
    @property
    def text(self):
#         return self.element.get_attribute("value")
        script = "return arguments[0].value;"
        return self.element._parent.execute_script(script, self.element)
    
    @text.setter
    def text(self, value):
#         self.element.set_attribute("value", value)
        value = utilities.js_string_encode(value)
        script= "return arguments[0].value = '%s';" % value
        self.element._parent.execute_script(script, self.element)
        
def Editor(webelement):
    """
    Constructor. A check is made that the given element is, indeed, a 
    INPUT/TEXTAREA tag. If it is not, then an UnexpectedTagNameException 
    is thrown.

    :Args:
     - webelement - element INPUT/TEXTAREA element to wrap
    
    Example:
        from selenium.webdriver.support.ui import Select \n
        Select(driver.find_element_by_tag_name("select")).select_by_index(2)
    """
    accepted_classes = [Input, TextArea]
    result = None
    for aclass in accepted_classes:
        try:
            result = aclass(webelement)
        except UnexpectedTagNameException:
            continue
        
        break
             
    if result is None:
        raise UnexpectedTagNameException("Not acceptable tag as Editor !")
        
    return result
        
    
    
