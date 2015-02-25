'''
@date 2014-11-16
@author Hong-she Liang <starofrainnight@gmail.com>
'''

def js_string_encode(text):
    result = []
    convert_table = {'\\':'\\\\', '\n':'\\n', '\r':'\\r', '\t':'\\t', 
                     '"':'\\"', "'":"\\'"}
    for character in text:
        for k, v in convert_table.iteritems():
            if character != k:
                continue
            
            character = v
            break
        
        result.append(character)
        
    return ''.join(result)
    
        