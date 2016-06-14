'''
@date 2015-02-21
@author Hong-She Liang <starofrainnight@gmail.com>
'''

import os
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
        '!': ['alt'],
        '+': ['shift'],
        '^': ['ctrl'],
        '#': ['Meta'],
    }

    __key_contexts = {
        # You must translate the virtual key code to scancdoe while using keybd_event.
        # key symbol:
        #   win32 virtual key code
        'SPACE': ['space'],
        'ENTER': ['Return'],
        'CTRL': ['ctrl'],
        'LCTRL': ['Control_L'],
        'RCTRL': ['Control_R'],
        'ALT': ['alt'],
        'LALT': ['Alt_L'],
        'RALT': ['Alt_R'],
        'SHIFT': ['shift'],
        'LSHIFT': ['Shift_L'],
        'RSHIFT': ['Shift_R'],
        'BACKSPACE': ['BackSpace'],
        'DELETE': ['Delete'],
        'UP': ['Up'],
        'DOWN': ['Down'],
        'LEFT': ['Left'],
        'RIGHT': ['Right'],
        'HOME': ['Home'],
        'END': ['End'],
        'ESCAPE': ['Escape'],
        'INSERT': ['Insert'],
        'CLEAR': ['Clear'],
        #     'OEM_CLEAR':['Clear'],
        'PGUP': ['Page_Up'],
        'PGDN': ['Page_Down'],
        'NUMLOCK': ['Num_Lock'],
        'CAPSLOCK': ['Caps_Lock'],
        'SCROLLLOCK': ['Scroll_Lock'],
        'SELECT': ['Select'],
        #     'SLEEP':[0x5F],
        'EXECUTE': ['Execute'],
        'HELP': ['Help'],
        #     'APPS':[win32con.VK_APPS],
        'F1': ['F1'],
        'F2': ['F2'],
        'F3': ['F3'],
        'F4': ['F4'],
        'F5': ['F5'],
        'F6': ['F6'],
        'F7': ['F7'],
        'F8': ['F8'],
        'F9': ['F9'],
        'F10': ['F10'],
        'F11': ['F11'],
        'F12': ['F12'],
        'F13': ['F13'],
        'F14': ['F14'],
        'F15': ['F15'],
        'F16': ['F16'],
        'F17': ['F17'],
        'F18': ['F18'],
        'F19': ['F19'],
        'F20': ['F20'],
        'F21': ['F21'],
        'F22': ['F22'],
        'F23': ['F23'],
        'F24': ['F24'],
        'TAB': ['Tab'],
        'PRINTSCREEN': ['Print'],
        'WIN': ['Meta'],
        'LWIN': ['Meta_L'],
        'RWIN': ['Meta_R'],
        'BREAK': ['Break'],
        'PAUSE': ['Pause'],
        'NUMPAD0': ['KP_0'],
        'NUMPAD1': ['KP_1'],
        'NUMPAD2': ['KP_2'],
        'NUMPAD3': ['KP_3'],
        'NUMPAD4': ['KP_4'],
        'NUMPAD5': ['KP_5'],
        'NUMPAD6': ['KP_6'],
        'NUMPAD7': ['KP_7'],
        'NUMPAD8': ['KP_8'],
        'NUMPAD9': ['KP_9'],
        'NUMPADMULT': ['KP_Multiply'],
        'NUMPADADD': ['KP_Add'],  # VK_OEM_PLUS, win32con.VK_ADD
        'NUMPADSUB': ['KP_Subtract'],  # VK_OEM_MINUS, win32con.VK_SUBTRACT
        'NUMPADDIV': ['KP_Divide'],
        'NUMPADDOT': ['KP_Separator'],  # VK_OEM_PERIOD
        'NUMPADENTER': ['KP_Enter'],

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
        ' ': ['space'],
        ';': ['semicolon'],  # VK_OEM_1, ;:
        ':': ['colon'],
        '/': ['slash'],  # VK_OEM_2, /?
        '?': ['question'],
        '`': ['grave'],  # VK_OEM_3, `~
        '~': ['asciitilde'],
        '[': ['bracketleft'],  # VK_OEM_4, [{
        '{': ['braceleft'],
        '\\': ['backslash'],  # VK_OEM_5, \|
        '|': ['bar'],
        ']': ['bracketright'],  # VK_OEM_6, ]}
        '}': ['braceright'],
        '\'': ['apostrophe'],  # VK_OEM_7, 'single-quote/double-quote'
        '"': ['quotedbl'],
        '0': ['0'],  # char
        ')': ['parenright'],
        '1': ['1'],  # char
        '!': ['exclam'],
        '2': ['2'],  # char
        '@': ['at'],
        '3': ['3'],  # char
        '#': ['numbersign'],
        '4': ['4'],  # char
        '$': ['dollar'],
        '5': ['5'],  # char
        '%': ['percent'],
        '6': ['6'],  # char
        '^': ['asciicircum'],
        '7': ['7'],  # char
        '&': ['ampersand'],
        '8': ['8'],  # char
        '*': ['asterisk'],
        '9': ['9'],  # char
        '(': ['parenleft'],
        '-': ['minus'],  # -_ , win32con.VK_SUBTRACT only means '-'
        '_': ['underscore'],
        ',': ['comma'],  # VK_OEM_COMMA, ,<
        '<': ['less'],
        '.': ['period'],  # VK_OEM_PERIOD, .>
        '>': ['greater'],
        '=': ['equal'],  # VK_OEM_PLUS, =+
        '+': ['plus'],
        'a': ['a'],
        'b': ['b'],
        'c': ['c'],
        'd': ['d'],
        'e': ['e'],
        'f': ['f'],
        'g': ['g'],
        'h': ['h'],
        'i': ['i'],
        'j': ['j'],
        'k': ['k'],
        'l': ['l'],
        'm': ['m'],
        'n': ['n'],
        'o': ['o'],
        'p': ['p'],
        'q': ['q'],
        'r': ['r'],
        's': ['s'],
        't': ['t'],
        'u': ['u'],
        'v': ['v'],
        'w': ['w'],
        'x': ['x'],
        'y': ['y'],
        'z': ['z'],

        'A': ['A'],
        'B': ['B'],
        'C': ['C'],
        'D': ['D'],
        'E': ['E'],
        'F': ['F'],
        'G': ['G'],
        'H': ['H'],
        'I': ['I'],
        'J': ['J'],
        'K': ['K'],
        'L': ['L'],
        'M': ['M'],
        'N': ['N'],
        'O': ['O'],
        'P': ['P'],
        'Q': ['Q'],
        'R': ['R'],
        'S': ['S'],
        'T': ['T'],
        'U': ['U'],
        'V': ['V'],
        'W': ['W'],
        'X': ['X'],
        'Y': ['Y'],
        'Z': ['Z'],
    }
    # Other keys are pass by ord(k)

    def __init__(self):
        super(Keyboard, self).__init__()
        self._target_window = ""

    @property
    def special_key_contexts(self):
        return self.__special_key_contexts

    @property
    def key_contexts(self):
        return self.__key_contexts

    def _send_method(self, action, context, **kwargs):
        '''
        @return If successed, return (0, None), otherwise return
        (1, Next Send Analyse Text) .
        '''

        key_text = context[0]

        options = ""
        if ('window' in kwargs) and (kwargs['window'] is not None):
            options = "--window %s" % kwargs['window']

        if action == KeyAction.press_hold:
            os.system("xdotool keydown %s %s" % (options, key_text))
        elif action == KeyAction.up:
            os.system("xdotool keyup %s %s" % (options, key_text))
        elif action == KeyAction.down:
            os.system("xdotool keydown %s %s" % (options, key_text))
        else:  # press and others.
            os.system("xdotool keydown %s %s" % (options, key_text))
            os.system("xdotool keyup %s %s" % (options, key_text))

        return (0, None)
