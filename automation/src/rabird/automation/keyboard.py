# -*- coding: UTF-8 -*-

#--IMPORT_ALL_FROM_FUTURE--#

'''
Created on 2013-7-7

@author: "HongShe Liang <starofrainnight@gmail.com>"
'''

import win32api
import win32con
import win32gui
import struct

try:
	# Use pywinio to emulate our keyboard if existed. 
	from . import winio_keyboard
	
	__send_method = winio_keyboard.keybd_event 
except ImportError as e:
	__send_method = win32api.keybd_event

# Without keys listed below :
#
#	{NUMLOCK on} NUMLOCK (on/off/toggle) 
#	{CAPSLOCK off} CAPSLOCK (on/off/toggle) 
#	{SCROLLLOCK toggle} SCROLLLOCK (on/off/toggle) 
#	{APPSKEY} Windows App key 
#	{LALT} Left ALT key 
#	{RALT} Right ALT key 
#	{LCTRL} Left CTRL key 
#	{RCTRL} Right CTRL key 
#	{LSHIFT} Left Shift key 
#	{RSHIFT} Right Shift key 
#	{SLEEP} Computer SLEEP key 
#	{ALTDOWN} Holds the ALT key down until {ALTUP} is sent 
#	{SHIFTDOWN} Holds the SHIFT key down until {SHIFTUP} is sent 
#	{CTRLDOWN} Holds the CTRL key down until {CTRLUP} is sent 
#	{LWINDOWN} Holds the left Windows key down until {LWINUP} is sent 
#	{RWINDOWN} Holds the right Windows key down until {RWINUP} is sent 
#	{ASC nnnn} Send the ALT+nnnn key combination 
#	{BROWSER_BACK} 2000/XP Only: Select the browser "back" button 
#	{BROWSER_FORWARD} 2000/XP Only: Select the browser "forward" button 
#	{BROWSER_REFRESH} 2000/XP Only: Select the browser "refresh" button 
#	{BROWSER_STOP} 2000/XP Only: Select the browser "stop" button 
#	{BROWSER_SEARCH} 2000/XP Only: Select the browser "search" button 
#	{BROWSER_FAVORITES} 2000/XP Only: Select the browser "favorites" button 
#	{BROWSER_HOME} 2000/XP Only: Launch the browser and go to the home page 
#	{VOLUME_MUTE} 2000/XP Only: Mute the volume 
#	{VOLUME_DOWN} 2000/XP Only: Reduce the volume 
#	{VOLUME_UP} 2000/XP Only: Increase the volume 
#	{MEDIA_NEXT} 2000/XP Only: Select next track in media player 
#	{MEDIA_PREV} 2000/XP Only: Select previous track in media player 
#	{MEDIA_STOP} 2000/XP Only: Stop media player 
#	{MEDIA_PLAY_PAUSE} 2000/XP Only: Play/pause media player 
#	{LAUNCH_MAIL} 2000/XP Only: Launch the email application 
#	{LAUNCH_MEDIA} 2000/XP Only: Launch media player 
#	{LAUNCH_APP1} 2000/XP Only: Launch user app1 
#	{LAUNCH_APP2} 2000/XP Only: Launch user app2
special_key_contexts = { 
	'!':[win32con.VK_MENU, 1, 0],
	'+':[win32con.VK_SHIFT, 1, 0],
	'^':[win32con.VK_CONTROL, 1, 0],
	'#':[win32con.VK_LWIN, 1, 0],
	}

key_contexts = {
	# You must translate the virtual key code to scancdoe while using keybd_event.
	# key symbol: 
	#   win32 virtual key code
	#   is hold until a key group pressed?
	#   is extended key?
	'SPACE':[win32con.VK_SPACE, 0, 0],
	'ENTER':[win32con.VK_RETURN, 0, 0],
	'ALT':[win32con.VK_MENU, 0, 0],
	'BACKSPACE':[win32con.VK_BACK, 0, 1],
	'DELETE':[win32con.VK_DELETE,  0, 1],
	'UP':[win32con.VK_UP, 0, 1],
	'DOWN':[win32con.VK_DOWN, 0, 1],
	'LEFT':[win32con.VK_LEFT, 0, 1],
	'RIGHT':[win32con.VK_RIGHT, 0, 1],
	'HOME':[win32con.VK_HOME, 0, 1],
	'END':[win32con.VK_END, 0, 1],
	'ESCAPE':[win32con.VK_ESCAPE, 0, 0],
	'INSERT':[win32con.VK_INSERT, 0, 1],
	'PGUP':[win32con.VK_PRIOR, 0, 1],
	'PGDN':[win32con.VK_NEXT, 0, 1],
	'F1':[win32con.VK_F1, 0, 0],
	'F2':[win32con.VK_F2, 0, 0],
	'F3':[win32con.VK_F3, 0, 0],
	'F4':[win32con.VK_F4, 0, 0],
	'F5':[win32con.VK_F5, 0, 0],
	'F6':[win32con.VK_F6, 0, 0],
	'F7':[win32con.VK_F7, 0, 0],
	'F8':[win32con.VK_F8, 0, 0],
	'F9':[win32con.VK_F9, 0, 0],
	'F10':[win32con.VK_F10, 0, 0],
	'F11':[win32con.VK_F11, 0, 0],
	'F12':[win32con.VK_F12, 0, 0],
	'F13':[win32con.VK_F13, 0, 0],
	'F14':[win32con.VK_F14, 0, 0],
	'F15':[win32con.VK_F15, 0, 0],
	'F16':[win32con.VK_F16, 0, 0],
	'F17':[win32con.VK_F17, 0, 0],
	'F18':[win32con.VK_F18, 0, 0],
	'F19':[win32con.VK_F19, 0, 0],
	'F20':[win32con.VK_F20, 0, 0],
	'F21':[win32con.VK_F21, 0, 0],
	'F22':[win32con.VK_F22, 0, 0],
	'F23':[win32con.VK_F23, 0, 0],
	'F24':[win32con.VK_F24, 0, 0],
	'TAB':[win32con.VK_TAB, 0, 0],
	'PRINTSCREEN':[win32con.VK_PRINT, 0, 0],
	'LWIN':[win32con.VK_LWIN, 0, 0],
	'RWIN':[win32con.VK_RWIN, 0, 0],
	'BREAK':[win32con.VK_CANCEL, 0, 0],
	'PAUSE':[win32con.VK_PAUSE, 0, 0],
	'NUMPAD0':[win32con.VK_NUMPAD0, 0, 0],
	'NUMPAD1':[win32con.VK_NUMPAD1, 0, 0],
	'NUMPAD2':[win32con.VK_NUMPAD2, 0, 0],
	'NUMPAD3':[win32con.VK_NUMPAD3, 0, 0],
	'NUMPAD4':[win32con.VK_NUMPAD4, 0, 0],
	'NUMPAD5':[win32con.VK_NUMPAD5, 0, 0],
	'NUMPAD6':[win32con.VK_NUMPAD6, 0, 0],
	'NUMPAD7':[win32con.VK_NUMPAD7, 0, 0],
	'NUMPAD8':[win32con.VK_NUMPAD8, 0, 0],
	'NUMPAD9':[win32con.VK_NUMPAD9, 0, 0],
	'NUMPADMULT':[win32con.VK_MULTIPLY, 0, 0],
	'NUMPADADD':[0xBB, 0, 0], # VK_OEM_PLUS, win32con.VK_ADD
	'NUMPADSUB':[0xBD, 0, 0], # VK_OEM_MINUS, win32con.VK_SUBTRACT
	'NUMPADDIV':[win32con.VK_DIVIDE, 0, 0],
	'NUMPADDOT':[0xBE, 0, 0], # VK_OEM_PERIOD
	'NUMPADENTER':[win32con.VK_RETURN, 0, 0],
	
	# Double function keys : 
	# for example : "[{", the "{" will appear while press Shift+[ .
	';':[0xBA, 0, 0], # VK_OEM_1, ;:
	':':['+;', 0, 0],
	'/':[0xBF, 0, 0], # VK_OEM_2, /?
	'?':['+/', 0, 0],
	'`':[0xC0, 0, 0], # VK_OEM_3, `~
	'~':['+`', 0, 0],
	'[':[0xDB, 0, 0], # VK_OEM_4, [{
	'{':['+[', 0, 0],
	'\\':[0xDC, 0, 0], # VK_OEM_5, \|
	'|':['+\\', 0, 0],
	']':[0xDD, 0, 0], # VK_OEM_6, ]}
	'}':['+]', 0, 0],
	'\'':[0xDE, 0, 0], # VK_OEM_7, 'single-quote/double-quote'
	'"':['+\'', 0, 0],
	'0':[ord('0'), 0, 0], # char
	')':['+0', 0, 0],
	'1':[ord('1'), 0, 0], # char
	'!':['+1', 0, 0],
	'2':[ord('2'), 0, 0], # char
	'@':['+2', 0, 0],
	'3':[ord('3'), 0, 0], # char
	'#':['+3', 0, 0],
	'4':[ord('4'), 0, 0], # char
	'$':['+4', 0, 0],
	'5':[ord('5'), 0, 0], # char
	'%':['+5', 0, 0],
	'6':[ord('6'), 0, 0], # char
	'^':['+6', 0, 0],
	'7':[ord('7'), 0, 0], # char
	'&':['+7', 0, 0],
	'8':[ord('8'), 0, 0], # char
	'*':['+8', 0, 0],
	'9':[ord('9'), 0, 0], # char
	'(':['+9', 0, 0],
	'-':[win32con.VK_SUBTRACT, 0, 0], # -_
	'_':['+-', 0, 0],
	',':[0xBC, 0, 0], # VK_OEM_COMMA, ,<
	'<':['+,', 0, 0],
	'.':[0xBE, 0, 0], # VK_OEM_PERIOD, .>
	'>':['+.', 0, 0],
	'=':[0xBB, 0, 0], # VK_OEM_PLUS, =+
	'+':['+=', 0, 0],
	'a':[ord('A'), 0, 0],
	'b':[ord('B'), 0, 0], 
	'c':[ord('C'), 0, 0], 
	'd':[ord('D'), 0, 0], 
	'e':[ord('E'), 0, 0], 
	'f':[ord('F'), 0, 0], 
	'g':[ord('G'), 0, 0], 
	'h':[ord('H'), 0, 0], 
	'i':[ord('I'), 0, 0], 
	'j':[ord('J'), 0, 0], 
	'k':[ord('K'), 0, 0], 
	'l':[ord('L'), 0, 0], 
	'm':[ord('M'), 0, 0], 
	'n':[ord('N'), 0, 0], 
	'o':[ord('O'), 0, 0],
	'p':[ord('P'), 0, 0],  
	'q':[ord('Q'), 0, 0],  
	'r':[ord('R'), 0, 0],  
	's':[ord('S'), 0, 0],  
	't':[ord('T'), 0, 0],  
	'u':[ord('U'), 0, 0],  
	'v':[ord('V'), 0, 0],  
	'w':[ord('W'), 0, 0],  
	'x':[ord('X'), 0, 0],  
	'y':[ord('Y'), 0, 0],
	'z':[ord('Z'), 0, 0],  
	
	'A':['+a', 0, 0],
	'B':['+b', 0, 0],
	'C':['+c', 0, 0],
	'D':['+d', 0, 0],
	'E':['+e', 0, 0],
	'F':['+f', 0, 0],
	'G':['+g', 0, 0],
	'H':['+h', 0, 0],
	'I':['+i', 0, 0],
	'J':['+j', 0, 0],
	'K':['+k', 0, 0],
	'L':['+l', 0, 0],
	'M':['+m', 0, 0],
	'N':['+n', 0, 0],
	'O':['+o', 0, 0],
	'P':['+p', 0, 0],
	'Q':['+q', 0, 0],
	'R':['+r', 0, 0],
	'S':['+s', 0, 0],
	'T':['+t', 0, 0],
	'U':['+u', 0, 0],
	'V':['+v', 0, 0],
	'W':['+w', 0, 0],
	'X':['+x', 0, 0],
	'Y':['+y', 0, 0],
	'Z':['+a', 0, 0],
	}
	# Other keys are pass by ord(k)
	
##
# Split a solo key series from keys beginning .
#
# @return [[context, length], ...]
def get_solo_key_series(keys, i=0):
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
			
			key = keys[i + 1:right_brace_pos]
			context = key_contexts[key]
			key_series.append([context, right_brace_pos - i + 1])
			i = right_brace_pos + 1
			return key_series
		elif key in special_key_contexts:
			context = special_key_contexts[key] 
			key_series.append([context, len(key)])
			i += len(key)
		else:
			context = key_contexts[key]
			key_series.append([context, len(key)])
			i += len(key)
			return key_series
		
	return key_series
	
def __send(keys, flags = 0):
	global __send_method
	
	i = 0
	while i < len(keys):
		key_series = get_solo_key_series(keys, i)
		command_end_queue = []
		for key_group in key_series:
			context = key_group[0]
			i += key_group[1]
			
			vkcode = context[0]
			is_holded = context[1]
			
			if int == type(vkcode):
				scancode = win32api.MapVirtualKey(vkcode, 0)
				# MAPVK_VK_TO_VSC_EX  = 4
				extended_scancode = win32api.MapVirtualKey(vkcode, 4)
				
				flags = 0
				if scancode != extended_scancode:
					flags |= win32con.KEYEVENTF_EXTENDEDKEY
					scancode = extended_scancode
					
				win32api.keybd_event(vkcode, scancode, flags)
				if is_holded:
					command_end_queue.append([vkcode, scancode, flags | win32con.KEYEVENTF_KEYUP])
				else:
					__send_method(vkcode, scancode, flags | win32con.KEYEVENTF_KEYUP)
			else:
				__send(vkcode, __send_method, flags)
		
		for command in command_end_queue:
			__send_method(command[0], command[1], command[2])

def send(keys):
	__send(keys)
