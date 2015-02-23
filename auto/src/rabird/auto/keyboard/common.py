'''
@date 2015-02-20
@author Hong-She Liang <starofrainnight@gmail.com>
'''

# Key Actions
(KA_UP, 
KA_DOWN,
KA_PRESS,
KA_ON,
KA_OFF,
KA_PRESS_HOLD) = xrange(0, 6)

class Keyboard(object):
    __key_action_map = dict()
    __key_action_map['up'] = KA_UP
    __key_action_map['down'] = KA_DOWN
    __key_action_map['press'] = KA_PRESS
    __key_action_map['on'] = KA_ON
    __key_action_map['off'] = KA_OFF
        
    def __init__(self):
        pass
        
    @property
    def special_key_contexts(self):
        raise NotImplemented()
    
    @property
    def key_contexts(self):
        raise NotImplemented()
    
    def _send_method(self, action, context):
        raise NotImplemented()
    
    def string_to_action(self, astr):
        return self.__key_action_map[astr.lower()]

    ##
    # Split a solo key series from keys beginning .
    #
    # @return [[context, length, action], ...]
    def get_solo_key_series(self, keys, i=0):
        key_series = []
            
        while i < len(keys):
            key = keys[i]
            
            if key == '{':
                # Search '}'
                right_brace_pos = keys.find('}', i)
                if right_brace_pos == -1:
                    raise SyntaxError('''Can't find match brace "}" for "{" at ''' + str(i))
                
                if (right_brace_pos - i) == 1:
                    right_brace_pos = keys.find('}', right_brace_pos + 1)
                    if right_brace_pos == -1:
                        raise SyntaxError('''Can't find match brace "}" for "{" at ''' + str(i))
                
                description = keys[i + 1:right_brace_pos]
                description_parts = description.split()
                key = description_parts[0]
                
                action = None
                if len(description_parts) > 1:
                    # up/down/on/off/toggle control
                    action = self.string_to_action(description_parts[1])
                    
                context = self.key_contexts[key]
                key_series.append([context, right_brace_pos - i + 1, action])
                i = right_brace_pos + 1
                return key_series
            elif key in self.special_key_contexts:
                context = self.special_key_contexts[key] 
                key_series.append([context, len(key), KA_PRESS_HOLD])
                i += len(key)
            else:
                context = self.key_contexts[key]
                key_series.append([context, len(key), KA_PRESS])
                i += len(key)
                return key_series
            
        return key_series
        
    def __send(self, keys):
        i = 0
        while i < len(keys):
            key_series = self.get_solo_key_series(keys, i)
            command_end_queue = []
            for key_group in key_series:
                context = key_group[0]
                i += key_group[1]
                action = key_group[2]
                
                send_result = self._send_method(action, context)
                if send_result[0] == 0:
                    if action == KA_PRESS_HOLD:
                        command_end_queue.append([KA_UP, context])
                else:
                    self.__send(send_result[1])
            
            for command_index in xrange(len(command_end_queue) -1, -1, -1):
                command = command_end_queue[command_index]
                self._send_method(*command)
    
    def send(self, keys, is_raw=False):
        if is_raw:
            new_keys = ''
            for c in keys:
                if c == ' ': # Space use to split description parts
                    new_keys += c
                else:
                    new_keys += '{%s}' % (c)
            
            self.__send(new_keys)
        else:
            self.__send(keys)
            
