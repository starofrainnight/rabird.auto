'''
@date 2015-02-21
@author Hong-She Liang <starofrainnight@gmail.com>
'''

import os
# Import the uinput unit, not our uinput .
uinput = __import__('uinput')
from . import common
from .common import KeyAction

class Keyboard(common.Keyboard):
    # Without keys listed below :
    #
    #    {ASC nnnn} Send the ALT+nnnn key combination 
    #    {BROWSER_BACK} 2000/XP Only: Select the browser "back" button 
    #    {BROWSER_FORWARD} 2000/XP Only: Select the browser "forward" button 
    #    {BROWSER_REFRESH} 2000/XP Only: Select the browser "refresh" button 
    #    {BROWSER_STOP} 2000/XP Only: Select the browser "stop" button 
    #    {BROWSER_SEARCH} 2000/XP Only: Select the browser "search" button 
    #    {BROWSER_FAVORITES} 2000/XP Only: Select the browser "favorites" button 
    #    {BROWSER_HOME} 2000/XP Only: Launch the browser and go to the home page 
    #    {VOLUME_MUTE} 2000/XP Only: Mute the volume 
    #    {VOLUME_DOWN} 2000/XP Only: Reduce the volume 
    #    {VOLUME_UP} 2000/XP Only: Increase the volume 
    #    {MEDIA_NEXT} 2000/XP Only: Select next track in media player 
    #    {MEDIA_PREV} 2000/XP Only: Select previous track in media player 
    #    {MEDIA_STOP} 2000/XP Only: Stop media player 
    #    {MEDIA_PLAY_PAUSE} 2000/XP Only: Play/pause media player 
    #    {LAUNCH_MAIL} 2000/XP Only: Launch the email application 
    #    {LAUNCH_MEDIA} 2000/XP Only: Launch media player 
    #    {LAUNCH_APP1} 2000/XP Only: Launch user app1 
    #    {LAUNCH_APP2} 2000/XP Only: Launch user app2
    __special_key_contexts = { 
        '!':[uinput.KEY_LEFTALT],
        '+':[uinput.KEY_LEFTSHIFT],
        '^':[uinput.KEY_LEFTCTRL],
        '#':[uinput.KEY_LEFTMETA],
        }
    
    __key_contexts = {
        # You must translate the virtual key code to scancdoe while using keybd_event.
        # key symbol: 
        #   win32 virtual key code
        'SPACE':[uinput.KEY_SPACE],
        'ENTER':[uinput.KEY_ENTER],
        'CTRL':[uinput.KEY_LEFTCTRL],
        'LCTRL':[uinput.KEY_LEFTCTRL],
        'RCTRL':[uinput.KEY_RIGHTCTRL],
        'ALT':[uinput.KEY_LEFTALT],
        'LALT':[uinput.KEY_LEFTALT],
        'RALT':[uinput.KEY_RIGHTALT],
        'SHIFT':[uinput.KEY_LEFTSHIFT],
        'LSHIFT':[uinput.KEY_LEFTSHIFT],
        'RSHIFT':[uinput.KEY_RIGHTSHIFT],
        'BACKSPACE':[uinput.KEY_BACKSPACE],
        'DELETE':[uinput.KEY_DELETE],
        'UP':[uinput.KEY_UP],
        'DOWN':[uinput.KEY_DOWN],
        'LEFT':[uinput.KEY_LEFT],
        'RIGHT':[uinput.KEY_RIGHT],
        'HOME':[uinput.KEY_HOME],
        'END':[uinput.KEY_END],
        'ESCAPE':[uinput.KEY_ESC],
        'INSERT':[uinput.KEY_INSERT],
        'CLEAR':[uinput.KEY_CLEAR],
    #     'OEM_CLEAR':['Clear'],        
        'PGUP':[uinput.KEY_PAGEUP],
        'PGDN':[uinput.KEY_PAGEDOWN],
        'NUMLOCK':[uinput.KEY_NUMLOCK],
        'CAPSLOCK':[uinput.KEY_CAPSLOCK],
        'SCROLLLOCK':[uinput.KEY_SCROLLLOCK],
        'SELECT':[uinput.KEY_SELECT],
    #     'SLEEP':[0x5F],
    #    'EXECUTE':['Execute'],
        'HELP':[uinput.KEY_HELP],
    #     'APPS':[win32con.VK_APPS],
        'F1':[uinput.KEY_F1],
        'F2':[uinput.KEY_F2],
        'F3':[uinput.KEY_F3],
        'F4':[uinput.KEY_F4],
        'F5':[uinput.KEY_F5],
        'F6':[uinput.KEY_F6],
        'F7':[uinput.KEY_F7],
        'F8':[uinput.KEY_F8],
        'F9':[uinput.KEY_F9],
        'F10':[uinput.KEY_F10],
        'F11':[uinput.KEY_F11],
        'F12':[uinput.KEY_F12],
        'F13':[uinput.KEY_F13],
        'F14':[uinput.KEY_F14],
        'F15':[uinput.KEY_F15],
        'F16':[uinput.KEY_F16],
        'F17':[uinput.KEY_F17],
        'F18':[uinput.KEY_F18],
        'F19':[uinput.KEY_F19],
        'F20':[uinput.KEY_F20],
        'F21':[uinput.KEY_F21],
        'F22':[uinput.KEY_F22],
        'F23':[uinput.KEY_F23],
        'F24':[uinput.KEY_F24],
        'TAB':[uinput.KEY_TAB],
        'PRINTSCREEN':[uinput.KEY_PRINT],
        'WIN':[uinput.KEY_LEFTMETA],
        'LWIN':[uinput.KEY_LEFTMETA],
        'RWIN':[uinput.KEY_RIGHTMETA],
        'BREAK':[uinput.KEY_BREAK],
        'PAUSE':[uinput.KEY_PAUSE],
        'NUMPAD0':[uinput.KEY_KP0],
        'NUMPAD1':[uinput.KEY_KP1],
        'NUMPAD2':[uinput.KEY_KP2],
        'NUMPAD3':[uinput.KEY_KP3],
        'NUMPAD4':[uinput.KEY_KP4],
        'NUMPAD5':[uinput.KEY_KP5],
        'NUMPAD6':[uinput.KEY_KP6],
        'NUMPAD7':[uinput.KEY_KP7],
        'NUMPAD8':[uinput.KEY_KP8],
        'NUMPAD9':[uinput.KEY_KP9],
        'NUMPADMULT':[uinput.KEY_NUMERIC_STAR],
        'NUMPADADD':[uinput.KEY_KPPLUS], # VK_OEM_PLUS, win32con.VK_ADD
        'NUMPADSUB':[uinput.KEY_KPMINUS], # VK_OEM_MINUS, win32con.VK_SUBTRACT
        'NUMPADDIV':[uinput.KEY_KPSLASH],
        'NUMPADDOT':[uinput.KEY_KPDOT], # VK_OEM_PERIOD
        'NUMPADENTER':[uinput.KEY_KPENTER],
        
    #     'PLAY':[win32con.VK_PLAY],
    #     'ZOOM':[win32con.VK_ZOOM],
    #     'PA1':[win32con.VK_PA1],
        
    #     'BROWSER_BACK':[win32con.VK_BROWSER_BACK],
    #     'BROWSER_FORWARD':[win32con.VK_BROWSER_FORWARD],
    #     'BROWSER_REFRESH':[0xA8],
    #     'BROWSER_STOP':[0xA9],
    #     'BROWSER_SEARCH':[0xAA],
    #     'BROWSER_FAVORITES':[0xAB],
    #     'BROWSER_HOME':[0xAC],
        
    #     'VOLUME_MUTE':[win32con.VK_VOLUME_MUTE],
    #     'VOLUME_DOWN':[win32con.VK_VOLUME_DOWN],
    #     'VOLUME_UP':[win32con.VK_VOLUME_UP],
        
    #     'MEDIA_NEXT_TRACK':[win32con.VK_MEDIA_NEXT_TRACK],
    #     'MEDIA_PREV_TRACK':[win32con.VK_MEDIA_PREV_TRACK],
    #     'MEDIA_STOP':[0xB2],
    #     'MEDIA_PLAY_PAUSE':[0xB3],
        
    #     'LAUNCH_MAIL':[0xB4],
    #     'LAUNCH_MEDIA_SELECT':[0xB5],
    #     'LAUNCH_APP1':[0xB6],
    #     'LAUNCH_APP2':[0xB7],
        
    #     'IME_KANA':[win32con.VK_KANA],
    #     'IME_HANGUL':[win32con.VK_HANGUL],
    #     'IME_JUNJA':[win32con.VK_JUNJA],
    #     'IME_FINAL':[win32con.VK_FINAL],
    #     'IME_HANJA':[win32con.VK_HANJA],
    #     'IME_KANJI':[win32con.VK_KANJI],
    #     'IME_CONVERT':[win32con.VK_CONVERT],
    #     'IME_NONCONVERT':[win32con.VK_NONCONVERT],
    #     'IME_ACCEPT':[win32con.VK_ACCEPT],
    #     'IME_MODECHANGE':[win32con.VK_MODECHANGE],
        
        # Double function keys : 
        # for example : "[{", the "{" will appear while press Shift+[ .
        ' ':[uinput.KEY_SPACE],
        ';':[uinput.KEY_SEMICOLON], # VK_OEM_1, ;:
        ':':['+;'],
        '/':[uinput.KEY_SLASH], # VK_OEM_2, /?
        '?':[uinput.KEY_QUESTION],
        '`':[uinput.KEY_GRAVE], # VK_OEM_3, `~
        '~':['+`'],
        '[':['+{'], # VK_OEM_4, [{
        '{':[uinput.KEY_LEFTBRACE],
        '\\':[uinput.KEY_BACKSLASH], # VK_OEM_5, \|
        '|':['+\\'],
        ']':['+}'], # VK_OEM_6, ]}
        '}':[uinput.KEY_RIGHTBRACE],
        '\'':[uinput.KEY_APOSTROPHE], # VK_OEM_7, 'single-quote/double-quote'
        '"':['+\''],
        '0':[uinput.KEY_0], # char
        ')':[uinput.KEY_KPRIGHTPAREN],
        '1':[uinput.KEY_1], # char
        '!':['+1'],
        '2':[uinput.KEY_2], # char
        '@':['+2'],
        '3':[uinput.KEY_3], # char
        '#':['+3'],
        '4':[uinput.KEY_4], # char
        '$':[uinput.KEY_DOLLAR],
        '5':[uinput.KEY_5], # char
        '%':['+5'],
        '6':[uinput.KEY_6], # char
        '^':['+6'],
        '7':[uinput.KEY_7], # char
        '&':['+7'],
        '8':[uinput.KEY_8], # char
        '*':['+8'],
        '9':[uinput.KEY_9], # char
        '(':[uinput.KEY_KPLEFTPAREN],
        '-':[uinput.KEY_MINUS], # -_ , win32con.VK_SUBTRACT only means '-'
        '_':['+-'],
        ',':[uinput.KEY_COMMA], # VK_OEM_COMMA, ,<
        '<':['+,'],
        '.':[uinput.KEY_DOT], # VK_OEM_PERIOD, .>
        '>':['+.'],
        '=':[uinput.KEY_EQUAL], # VK_OEM_PLUS, =+
        '+':['+='],
        'a':[uinput.KEY_A],
        'b':[uinput.KEY_B], 
        'c':[uinput.KEY_C], 
        'd':[uinput.KEY_D], 
        'e':[uinput.KEY_E], 
        'f':[uinput.KEY_F], 
        'g':[uinput.KEY_G], 
        'h':[uinput.KEY_H], 
        'i':[uinput.KEY_I], 
        'j':[uinput.KEY_J], 
        'k':[uinput.KEY_K], 
        'l':[uinput.KEY_L], 
        'm':[uinput.KEY_M], 
        'n':[uinput.KEY_N], 
        'o':[uinput.KEY_O],
        'p':[uinput.KEY_P],  
        'q':[uinput.KEY_Q],  
        'r':[uinput.KEY_R],  
        's':[uinput.KEY_S],  
        't':[uinput.KEY_T],  
        'u':[uinput.KEY_U],  
        'v':[uinput.KEY_V],  
        'w':[uinput.KEY_W],  
        'x':[uinput.KEY_X],  
        'y':[uinput.KEY_Y],
        'z':[uinput.KEY_Z],  
        
        'A':['+a'],
        'B':['+b'],
        'C':['+c'],
        'D':['+d'],
        'E':['+e'],
        'F':['+f'],
        'G':['+g'],
        'H':['+h'],
        'I':['+i'],
        'J':['+j'],
        'K':['+k'],
        'L':['+l'],
        'M':['+m'],
        'N':['+n'],
        'O':['+o'],
        'P':['+p'],
        'Q':['+q'],
        'R':['+r'],
        'S':['+s'],
        'T':['+t'],
        'U':['+u'],
        'V':['+v'],
        'W':['+w'],
        'X':['+x'],
        'Y':['+y'],
        'Z':['+z'],
        }
        # Other keys are pass by ord(k)
        
    def __init__(self):
        super(Keyboard, self).__init__()
        
        # Create a usb device to accept all events 
        events = []
        for v in list(uinput.ev.__dict__.values()):
            if type(v) == tuple:
                events.append(events)  
                
        self.__device = uinput.Device(events)
        
    @property
    def special_key_contexts(self):
        return self.__special_key_contexts
    
    @property
    def key_contexts(self):
        return self.__key_contexts
    
    def _send_method(self, action, context):
        '''
        @return If successed, return (0, None), otherwise return 
        (1, Next Send Analyse Text) . 
        '''
        vkcode = context[0]
        
        if tuple == type(vkcode):
            if action == KeyAction.press_hold:
                self.__device.emit(vkcode, 1)
            elif action == KeyAction.up:
                self.__device.emit(vkcode, 0)
            elif action == KeyAction.down:
                self.__device.emit(vkcode, 1)
            else: # press and others.
                self.__device.emit_click(vkcode)
            
            return (0, None)
        else:
            return (1, vkcode)
