'''
@date 2015-02-20
@author Hong-She Liang <starofrainnight@gmail.com>
'''

import win32con
import win32api
import win32gui
from . import common
from .common import KeyAction

try:
    # Use pywinio to emulate our keyboard if existed. 
    from . import keyboard_winio
    
    __keybd_event = keyboard_winio.keybd_event
except ImportError as e:
    __keybd_event = win32api.keybd_event
    
class Keyboard(common.Keyboard):
    '''
    Without keys listed below :
    
       {ASC nnnn} Send the ALT+nnnn key combination 
       {BROWSER_BACK} 2000/XP Only: Select the browser "back" button 
       {BROWSER_FORWARD} 2000/XP Only: Select the browser "forward" button 
       {BROWSER_REFRESH} 2000/XP Only: Select the browser "refresh" button 
       {BROWSER_STOP} 2000/XP Only: Select the browser "stop" button 
       {BROWSER_SEARCH} 2000/XP Only: Select the browser "search" button 
       {BROWSER_FAVORITES} 2000/XP Only: Select the browser "favorites" button 
       {BROWSER_HOME} 2000/XP Only: Launch the browser and go to the home page 
       {VOLUME_MUTE} 2000/XP Only: Mute the volume 
       {VOLUME_DOWN} 2000/XP Only: Reduce the volume 
       {VOLUME_UP} 2000/XP Only: Increase the volume 
       {MEDIA_NEXT} 2000/XP Only: Select next track in media player 
       {MEDIA_PREV} 2000/XP Only: Select previous track in media player 
       {MEDIA_STOP} 2000/XP Only: Stop media player 
       {MEDIA_PLAY_PAUSE} 2000/XP Only: Play/pause media player 
       {LAUNCH_MAIL} 2000/XP Only: Launch the email application 
       {LAUNCH_MEDIA} 2000/XP Only: Launch media player 
       {LAUNCH_APP1} 2000/XP Only: Launch user app1 
       {LAUNCH_APP2} 2000/XP Only: Launch user app2
    '''
    
    __special_key_contexts = { 
        '!':[win32con.VK_MENU],
        '+':[win32con.VK_SHIFT],
        '^':[win32con.VK_CONTROL],
        '#':[win32con.VK_LWIN],
        }
    
    __key_contexts = {
        # You must translate the virtual key code to scancdoe while using keybd_event.
        # key symbol: 
        #   win32 virtual key code
        'SPACE':[win32con.VK_SPACE],
        'ENTER':[win32con.VK_RETURN],
        'CTRL':[win32con.VK_CONTROL],
        'LCTRL':[win32con.VK_LCONTROL],
        'RCTRL':[win32con.VK_RCONTROL],
        'ALT':[win32con.VK_MENU],
        'LALT':[win32con.VK_LMENU],
        'RALT':[win32con.VK_RMENU],
        'SHIFT':[win32con.VK_SHIFT],
        'LSHIFT':[win32con.VK_LSHIFT],
        'RSHIFT':[win32con.VK_RSHIFT],
        'BACKSPACE':[win32con.VK_BACK],
        'DELETE':[win32con.VK_DELETE],
        'UP':[win32con.VK_UP],
        'DOWN':[win32con.VK_DOWN],
        'LEFT':[win32con.VK_LEFT],
        'RIGHT':[win32con.VK_RIGHT],
        'HOME':[win32con.VK_HOME],
        'END':[win32con.VK_END],
        'ESCAPE':[win32con.VK_ESCAPE],
        'INSERT':[win32con.VK_INSERT],
        'CLEAR':[win32con.VK_CLEAR],
        'OEM_CLEAR':[win32con.VK_OEM_CLEAR],        
        'PGUP':[win32con.VK_PRIOR],
        'PGDN':[win32con.VK_NEXT],
        'NUMLOCK':[win32con.VK_NUMLOCK],
        'CAPSLOCK':[win32con.VK_CAPITAL],
        'SCROLLLOCK':[win32con.VK_SCROLL],
        'SELECT':[win32con.VK_SELECT],
        'SLEEP':[0x5F],
        'EXECUTE':[win32con.VK_EXECUTE],
        'HELP':[win32con.VK_HELP],
        'APPS':[win32con.VK_APPS],
        'F1':[win32con.VK_F1],
        'F2':[win32con.VK_F2],
        'F3':[win32con.VK_F3],
        'F4':[win32con.VK_F4],
        'F5':[win32con.VK_F5],
        'F6':[win32con.VK_F6],
        'F7':[win32con.VK_F7],
        'F8':[win32con.VK_F8],
        'F9':[win32con.VK_F9],
        'F10':[win32con.VK_F10],
        'F11':[win32con.VK_F11],
        'F12':[win32con.VK_F12],
        'F13':[win32con.VK_F13],
        'F14':[win32con.VK_F14],
        'F15':[win32con.VK_F15],
        'F16':[win32con.VK_F16],
        'F17':[win32con.VK_F17],
        'F18':[win32con.VK_F18],
        'F19':[win32con.VK_F19],
        'F20':[win32con.VK_F20],
        'F21':[win32con.VK_F21],
        'F22':[win32con.VK_F22],
        'F23':[win32con.VK_F23],
        'F24':[win32con.VK_F24],
        'TAB':[win32con.VK_TAB],
        'PRINTSCREEN':[win32con.VK_PRINT],
        'WIN':[win32con.VK_LWIN],
        'LWIN':[win32con.VK_LWIN],
        'RWIN':[win32con.VK_RWIN],
        'BREAK':[win32con.VK_CANCEL],
        'PAUSE':[win32con.VK_PAUSE],
        'NUMPAD0':[win32con.VK_NUMPAD0],
        'NUMPAD1':[win32con.VK_NUMPAD1],
        'NUMPAD2':[win32con.VK_NUMPAD2],
        'NUMPAD3':[win32con.VK_NUMPAD3],
        'NUMPAD4':[win32con.VK_NUMPAD4],
        'NUMPAD5':[win32con.VK_NUMPAD5],
        'NUMPAD6':[win32con.VK_NUMPAD6],
        'NUMPAD7':[win32con.VK_NUMPAD7],
        'NUMPAD8':[win32con.VK_NUMPAD8],
        'NUMPAD9':[win32con.VK_NUMPAD9],
        'NUMPADMULT':[win32con.VK_MULTIPLY],
        'NUMPADADD':[0xBB], # VK_OEM_PLUS, win32con.VK_ADD
        'NUMPADSUB':[0xBD], # VK_OEM_MINUS, win32con.VK_SUBTRACT
        'NUMPADDIV':[win32con.VK_DIVIDE],
        'NUMPADDOT':[0xBE], # VK_OEM_PERIOD
        'NUMPADENTER':[win32con.VK_RETURN],
        
        'PLAY':[win32con.VK_PLAY],
        'ZOOM':[win32con.VK_ZOOM],
        'PA1':[win32con.VK_PA1],
        
        'BROWSER_BACK':[win32con.VK_BROWSER_BACK],
        'BROWSER_FORWARD':[win32con.VK_BROWSER_FORWARD],
        'BROWSER_REFRESH':[0xA8],
        'BROWSER_STOP':[0xA9],
        'BROWSER_SEARCH':[0xAA],
        'BROWSER_FAVORITES':[0xAB],
        'BROWSER_HOME':[0xAC],
        
        'VOLUME_MUTE':[win32con.VK_VOLUME_MUTE],
        'VOLUME_DOWN':[win32con.VK_VOLUME_DOWN],
        'VOLUME_UP':[win32con.VK_VOLUME_UP],
        
        'MEDIA_NEXT_TRACK':[win32con.VK_MEDIA_NEXT_TRACK],
        'MEDIA_PREV_TRACK':[win32con.VK_MEDIA_PREV_TRACK],
        'MEDIA_STOP':[0xB2],
        'MEDIA_PLAY_PAUSE':[0xB3],
        
        'LAUNCH_MAIL':[0xB4],
        'LAUNCH_MEDIA_SELECT':[0xB5],
        'LAUNCH_APP1':[0xB6],
        'LAUNCH_APP2':[0xB7],
        
        'IME_KANA':[win32con.VK_KANA],
        'IME_HANGUL':[win32con.VK_HANGUL],
        'IME_JUNJA':[win32con.VK_JUNJA],
        'IME_FINAL':[win32con.VK_FINAL],
        'IME_HANJA':[win32con.VK_HANJA],
        'IME_KANJI':[win32con.VK_KANJI],
        'IME_CONVERT':[win32con.VK_CONVERT],
        'IME_NONCONVERT':[win32con.VK_NONCONVERT],
        'IME_ACCEPT':[win32con.VK_ACCEPT],
        'IME_MODECHANGE':[win32con.VK_MODECHANGE],
        
        # Double function keys : 
        # for example : "[{", the "{" will appear while press Shift+[ .
        ' ':[win32con.VK_SPACE],
        ';':[0xBA], # VK_OEM_1, ;:
        ':':['+;'],
        '/':[0xBF], # VK_OEM_2, /?
        '?':['+/'],
        '`':[0xC0], # VK_OEM_3, `~
        '~':['+`'],
        '[':[0xDB], # VK_OEM_4, [{
        '{':['+['],
        '\\':[0xDC], # VK_OEM_5, \|
        '|':['+\\'],
        ']':[0xDD], # VK_OEM_6, ]}
        '}':['+]'],
        '\'':[0xDE], # VK_OEM_7, 'single-quote/double-quote'
        '"':['+\''],
        '0':[ord('0')], # char
        ')':['+0'],
        '1':[ord('1')], # char
        '!':['+1'],
        '2':[ord('2')], # char
        '@':['+2'],
        '3':[ord('3')], # char
        '#':['+3'],
        '4':[ord('4')], # char
        '$':['+4'],
        '5':[ord('5')], # char
        '%':['+5'],
        '6':[ord('6')], # char
        '^':['+6'],
        '7':[ord('7')], # char
        '&':['+7'],
        '8':[ord('8')], # char
        '*':['+8'],
        '9':[ord('9')], # char
        '(':['+9'],
        '-':[0xBD], # -_ , win32con.VK_SUBTRACT only means '-'
        '_':['+-'],
        ',':[0xBC], # VK_OEM_COMMA, ,<
        '<':['+,'],
        '.':[0xBE], # VK_OEM_PERIOD, .>
        '>':['+.'],
        '=':[0xBB], # VK_OEM_PLUS, =+
        '+':['+='],
        'a':[ord('A')],
        'b':[ord('B')], 
        'c':[ord('C')], 
        'd':[ord('D')], 
        'e':[ord('E')], 
        'f':[ord('F')], 
        'g':[ord('G')], 
        'h':[ord('H')], 
        'i':[ord('I')], 
        'j':[ord('J')], 
        'k':[ord('K')], 
        'l':[ord('L')], 
        'm':[ord('M')], 
        'n':[ord('N')], 
        'o':[ord('O')],
        'p':[ord('P')],  
        'q':[ord('Q')],  
        'r':[ord('R')],  
        's':[ord('S')],  
        't':[ord('T')],  
        'u':[ord('U')],  
        'v':[ord('V')],  
        'w':[ord('W')],  
        'x':[ord('X')],  
        'y':[ord('Y')],
        'z':[ord('Z')],  
        
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
        
        if int == type(vkcode):
            scancode = win32api.MapVirtualKey(vkcode, 0)
            # MAPVK_VK_TO_VSC_EX  = 4
            extended_scancode = win32api.MapVirtualKey(vkcode, 4)
            flags = 0
            if scancode != extended_scancode:
                flags |= win32con.KEYEVENTF_EXTENDEDKEY
                scancode = extended_scancode
            
            if action == KeyAction.press_hold:
                __keybd_event(vkcode, scancode, flags)
            elif action == KeyAction.up:
                __keybd_event(vkcode, scancode, flags | win32con.KEYEVENTF_KEYUP)
            elif action == KeyAction.down:
                __keybd_event(vkcode, scancode, flags)
            else: # press and others.
                __keybd_event(vkcode, scancode, flags)
                __keybd_event(vkcode, scancode, flags | win32con.KEYEVENTF_KEYUP)
            
            return (0, None)
        else:
            return (1, vkcode)
