# -*- coding: UTF-8 -*-

#--IMPORT_ALL_FROM_FUTURE--#

'''
Created on 2013-7-7

@author: "HongShe Liang <starofrainnight@gmail.com>"
'''

import struct
import os
import sys

if sys.platform == "win32":
	import win32api
	import win32con
	import win32gui
	from . import keyboard_win32
	
	try:
		# Use pywinio to emulate our keyboard if existed. 
		from . import keyboard_winio
		
		__send_method = keyboard_winio.keybd_event
	except ImportError as e:
		__send_method = win32api.keybd_event
		
	special_key_contexts = keyboard_win32.special_key_contexts
	key_contexts = keyboard_win32.key_contexts
	
# Key Actions
(KA_UP, 
KA_DOWN,
KA_PRESS,
KA_ON,
KA_OFF) = xrange(0, 5)

__key_action_map = dict()
__key_action_map['up'] = KA_UP
__key_action_map['down'] = KA_DOWN
__key_action_map['press'] = KA_PRESS
__key_action_map['on'] = KA_ON
__key_action_map['off'] = KA_OFF
	
def string_to_action(astr):
	global __key_action_map
	
	return __key_action_map[astr.lower()]
	
##
# Split a solo key series from keys beginning .
#
# @return [[context, length, action], ...]
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
			
			description = keys[i + 1:right_brace_pos]
			description_parts = description.split()
			key = description_parts[0]
			
			action = None
			if len(description_parts) > 1:
				# up/down/on/off/toggle control
				action = string_to_action(description_parts[1])
				
			context = key_contexts[key]
			key_series.append([context, right_brace_pos - i + 1, action])
			i = right_brace_pos + 1
			return key_series
		elif key in special_key_contexts:
			context = special_key_contexts[key] 
			key_series.append([context, len(key), KA_PRESS])
			i += len(key)
		else:
			context = key_contexts[key]
			key_series.append([context, len(key), KA_PRESS])
			i += len(key)
			return key_series
		
	return key_series
	
def __send(keys, flags=0):
	global __send_method
	
	i = 0
	while i < len(keys):
		key_series = get_solo_key_series(keys, i)
		command_end_queue = []
		for key_group in key_series:
			context = key_group[0]
			i += key_group[1]
			action = key_group[2]
			
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
				
				if is_holded:
					__send_method(vkcode, scancode, flags)
					command_end_queue.append([vkcode, scancode, flags | win32con.KEYEVENTF_KEYUP])
				elif action == KA_UP:
					__send_method(vkcode, scancode, flags | win32con.KEYEVENTF_KEYUP)
				elif action == KA_DOWN:
					__send_method(vkcode, scancode, flags)
				else: # press and others.
					__send_method(vkcode, scancode, flags)
					command_end_queue.append([vkcode, scancode, flags | win32con.KEYEVENTF_KEYUP])
			else:
				__send(vkcode, flags)
		
		for command_index in xrange(len(command_end_queue) -1, -1, -1):
			command = command_end_queue[command_index]
			__send_method(command[0], command[1], command[2])

def send(keys, is_raw=False):
	if is_raw:
		new_keys = ''
		for c in keys:
			if c == ' ': # Space use to split description parts
				new_keys += c
			else:
				new_keys += '{%s}' % (c)
		
		__send(new_keys)
	else:
		__send(keys)
