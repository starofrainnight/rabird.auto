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
    from . import winio
    
    _keybd_event = winio.keybd_event
except ImportError as e:
    _keybd_event = win32api.keybd_event
    
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
        
    # http://www.computer-engineering.org/ps2keyboard/
    # Scan Code Set 1 - Original XT scan code set; supported by some modern keyboards
    __ps2_vk_to_sc = {
        win32con.VK_SPACE:0x39,
        win32con.VK_RETURN:0x1C,
        win32con.VK_CONTROL:0x1D, 
        win32con.VK_LCONTROL:0x1D,
        win32con.VK_RCONTROL:0xE01D,
        win32con.VK_MENU:0x38, # ALT
        win32con.VK_LMENU:0x38, # ALT
        win32con.VK_RMENU:0xE038,
        win32con.VK_SHIFT:0x2A, # SHIFT
        win32con.VK_LSHIFT:0x2A,
        win32con.VK_RSHIFT:0x36,
        win32con.VK_BACK:0x0E,
        win32con.VK_DELETE:0xE053,
        win32con.VK_UP:0xE048,
        win32con.VK_DOWN:0xE050,
        win32con.VK_LEFT:0xE04B,
        win32con.VK_RIGHT:0xE04D,
        win32con.VK_HOME:0xE047,
        win32con.VK_END:0xE04F,
        win32con.VK_ESCAPE:0x01,
        win32con.VK_INSERT:0xE052,
#         'CLEAR':[win32con.VK_CLEAR],
#         'OEM_CLEAR':[win32con.VK_OEM_CLEAR],        
        win32con.VK_PRIOR:0xE049, # Page Up
        win32con.VK_NEXT:0xE051,
        win32con.VK_NUMLOCK:0x45,
        win32con.VK_CAPITAL:0x3A,
        win32con.VK_SCROLL:0x46,
#         'SELECT':[win32con.VK_SELECT],
        0x5F:0xE05F, # 'SLEEP'
#         'EXECUTE':[win32con.VK_EXECUTE],
#         'HELP':[win32con.VK_HELP],
        win32con.VK_APPS:0xE05D,
        win32con.VK_F1:0x3B,
        win32con.VK_F2:0x3C,
        win32con.VK_F3:0x3D,
        win32con.VK_F4:0x3E,
        win32con.VK_F5:0x3F,
        win32con.VK_F6:0x40,
        win32con.VK_F7:0x41,
        win32con.VK_F8:0x42,
        win32con.VK_F9:0x43,
        win32con.VK_F10:0x44,
        win32con.VK_F11:0x57,
        win32con.VK_F12:0x58,
        win32con.VK_TAB:0x0F,
        win32con.VK_PRINT:0xE02AE037,
        win32con.VK_LWIN:0xE05B, # WIN
        win32con.VK_RWIN:0xE05C,
#         'BREAK':[win32con.VK_CANCEL],
        win32con.VK_PAUSE:0xE11D45E19DC5,
        win32con.VK_NUMPAD0:0x52,
        win32con.VK_NUMPAD1:0x4F,
        win32con.VK_NUMPAD2:0x50,
        win32con.VK_NUMPAD3:0x51,
        win32con.VK_NUMPAD4:0x4B,
        win32con.VK_NUMPAD5:0x4C,
        win32con.VK_NUMPAD6:0x4D,
        win32con.VK_NUMPAD7:0x47,
        win32con.VK_NUMPAD8:0x48,
        win32con.VK_NUMPAD9:0x49,
        win32con.VK_MULTIPLY:0x37, # NUMPADMULT
        0xBB:0x4E, # VK_OEM_PLUS, win32con.VK_ADD
        0xBD:0x4A, # VK_OEM_MINUS, win32con.VK_SUBTRACT
        win32con.VK_DIVIDE:0xE035,
        0xBE:0x53, # VK_OEM_PERIOD
        win32con.VK_RETURN:0xE01C,
                
#         'PLAY':[win32con.VK_PLAY],
#         'ZOOM':[win32con.VK_ZOOM],
#         'PA1':[win32con.VK_PA1],
        
        win32con.VK_BROWSER_BACK:0xE06A, # BROWSER_BACK
        win32con.VK_BROWSER_FORWARD:0xE069,
        0xA8:0xE067, # BROWSER_REFRESH
        0xA9:0xE068, # BROWSER_STOP
        0xAA:0xE065, # BROWSER_SEARCH
        0xAB:0xE066, # BROWSER_FAVORITES
        0xAC:0xE032, # BROWSER_HOME
        
        win32con.VK_VOLUME_MUTE:0xE020,
        win32con.VK_VOLUME_DOWN:0xE02E,
        win32con.VK_VOLUME_UP:0xE030,
        
        win32con.VK_MEDIA_NEXT_TRACK:0xE019,
        win32con.VK_MEDIA_PREV_TRACK:0xE010,
        0xB2:0xE024, # MEDIA_STOP
        0xB3:0xE022, # MEDIA_PLAY_PAUSE
        
        0xB4: 0xE06C, # LAUNCH_MAIL
        0xB5: 0xE06D, # LAUNCH_MEDIA_SELECT
#         'LAUNCH_APP1':[0xB6],
#         'LAUNCH_APP2':[0xB7],
        
#         'IME_KANA':[win32con.VK_KANA],
#         'IME_HANGUL':[win32con.VK_HANGUL],
#         'IME_JUNJA':[win32con.VK_JUNJA],
#         'IME_FINAL':[win32con.VK_FINAL],
#         'IME_HANJA':[win32con.VK_HANJA],
#         'IME_KANJI':[win32con.VK_KANJI],
#         'IME_CONVERT':[win32con.VK_CONVERT],
#         'IME_NONCONVERT':[win32con.VK_NONCONVERT],
#         'IME_ACCEPT':[win32con.VK_ACCEPT],
#         'IME_MODECHANGE':[win32con.VK_MODECHANGE],
        
        0xBA:0x27, # VK_OEM_1, ;:
        0xBF:0x35, # VK_OEM_2, /?
        0xC0:0x29, # VK_OEM_3, `~
        ord('['):0x1A, # VK_OEM_4, [{
        0xDC:0x2B, # VK_OEM_5, \|
        0xDD:0x1B, # VK_OEM_6, ]}
        ord('\''):0x2B, # VK_OEM_7, 'single-quote/double-quote'
        ord('0'):0x0B, # char
        ord('1'):0x02, # char
        ord('2'):0x03, # char
        ord('3'):0x04, # char
        ord('4'):0x05, # char
        ord('5'):0x06, # char
        ord('6'):0x07, # char
        ord('7'):0x08, # char
        ord('8'):0x09, # char
        ord('9'):0x0A, # char
        ord('-'):0x0C, # -_ , win32con.VK_SUBTRACT only means '-'
        0xBC:0x33, # VK_OEM_COMMA, ,<
        0xBE:0x34, # VK_OEM_PERIOD, .>
        ord('='):0x0D, # VK_OEM_PLUS, =+
        ord('a'):0x1E,
        ord('b'):0x30,
        ord('c'):0x2E,
        ord('d'):0x20,
        ord('e'):0x12,
        ord('f'):0x21,
        ord('g'):0x22,
        ord('h'):0x23,
        ord('i'):0x17,
        ord('j'):0x24,
        ord('k'):0x25,
        ord('l'):0x26,
        ord('m'):0x32,
        ord('n'):0x31,
        ord('o'):0x18,
        ord('p'):0x19,
        ord('q'):0x10,
        ord('r'):0x13,
        ord('s'):0x1F,
        ord('t'):0x14,
        ord('u'):0x16,
        ord('v'):0x2F,
        ord('w'):0x11,
        ord('x'):0x2D,
        ord('y'):0x15,
        ord('z'):0x2C,
        }
        
    def __init__(self):
        super(Keyboard, self).__init__()

    @property
    def special_key_contexts(self):
        return self.__special_key_contexts
    
    @property
    def key_contexts(self):
        return self.__key_contexts
    
    def _ps2_vk_to_sc(self, vkcode):
        if vkcode in self.__ps2_vk_to_sc:
            return self.__ps2_vk_to_sc[vkcode]
        else:
            return 0
    
    def _send_method(self, action, context):
        '''
        @return If successed, return (0, None), otherwise return 
        (1, Next Send Analyse Text) . 
        '''
        
        vkcode = context[0]
        
        if int == type(vkcode):
            scancode = win32api.MapVirtualKey(vkcode, 0)
            # MAPVK_VK_TO_VSC_EX  = 4, returned high byte will be 0xE0 or 0xE1
            extended_scancode = win32api.MapVirtualKey(vkcode, 4, win32api.GetKeyboardLayout())
            flags = 0
            if scancode != extended_scancode:
                flags |= win32con.KEYEVENTF_EXTENDEDKEY
                scancode = extended_scancode
            
            if action == KeyAction.press_hold:
                _keybd_event(vkcode, scancode, flags)
            elif action == KeyAction.up:
                _keybd_event(vkcode, scancode, flags | win32con.KEYEVENTF_KEYUP)
            elif action == KeyAction.down:
                _keybd_event(vkcode, scancode, flags)
            else: # press and others.
                _keybd_event(vkcode, scancode, flags)
                _keybd_event(vkcode, scancode, flags | win32con.KEYEVENTF_KEYUP)
            
            return (0, None)
        else:
            return (1, vkcode)
