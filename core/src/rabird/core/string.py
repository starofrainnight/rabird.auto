'''
@date 2015-02-25
@author Hong-She Liang <starofrainnight@gmail.com>
'''

def cstring_encode(text):
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
    