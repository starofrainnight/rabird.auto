
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
        super(Input, self).__init__(webelement)
        
        if webelement.tag_name.lower() != "input":
            raise UnexpectedTagNameException("Input only works on <input> "
                                             "elements, not on <%s>" %
                                             webelement.tag_name)
            
    @property
    def text(self):
        script = "return arguments[0].value;"
        return self.element._parent.execute_script(script, self.element)
    
    @text.setter
    def text(self, value):
        value = utilities.js_string_encode(value)
        script= "arguments[0].value = '%s';" % value
        self.element._parent.execute_script(script, self.element)
        
class TextArea(BaseEditor):
    def __init__(self, webelement):
        super(TextArea, self).__init__(webelement)
        
        if webelement.tag_name.lower() != "textarea":
            raise UnexpectedTagNameException("TextArea only works on <textarea> "
                                             "elements, not on <%s>" % 
                                             webelement.tag_name)
            
    @property
    def text(self):
        script = "return arguments[0].value;"
        return self.element._parent.execute_script(script, self.element)
    
    @text.setter
    def text(self, value):
        value = utilities.js_string_encode(value)
        script= "arguments[0].value = '%s';" % value
        self.element._parent.execute_script(script, self.element)
        
class TinyMCE(BaseEditor):
    def __init__(self, webelement):
        super(TinyMCE, self).__init__(webelement)
        
        if (webelement.tag_name.lower() != "textarea"): 
            raise UnexpectedTagNameException("TinyMCE only works on <textarea> "
                                             "elements, not on <%s>" % 
                                             webelement.tag_name)
        editors = self.get_editors()
        id_value = webelement.get_attribute("id")
        if id_value is None:
            raise UnexpectedTagNameException("Textarea without 'id' attribute!")
        
        is_tinymce_editor = False
        for aeditor in editors:
            if aeditor == id_value:
                is_tinymce_editor = True
                break
            
        if not is_tinymce_editor:
            raise UnexpectedTagNameException("This textarea is not an TinyMCE editor !")
        
    def get_editors(self):
        script = """
        var editors = new Array()
        for (i in tinymce.editors) {
            editors[i] = tinymce.editors[i].id
        }
        return editors;
        """
        return self.element._parent.execute_script(script)
        
    @property
    def text(self):
        script = "return tinymce.get('%s').getContent();" % self.element.get_attribute("id")
        return self.element._parent.execute_script(script)
    
    @text.setter
    def text(self, value):
        value = utilities.js_string_encode(value)
        script= "tinymce.get('%s').setContent('%s', {format: 'raw'});" % (self.element.get_attribute("id"), value)
        self.element._parent.execute_script(script)
        
def Editor(webelement):
    # TinyMCE must before TextArea, because TinyMCE also a TextArea!
    accepted_classes = [Input, TinyMCE, TextArea]
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
        
    
    
