'''
Created on 2013-8-14

@author: "HongShe Liang <starofrainnight@gmail.com>"
'''

# -*- coding: UTF-8 -*-

#--IMPORT_ALL_FROM_FUTURE--#

import win32gui
import pywintypes
import time

# WindowTextMatchMode
(
WTMM_COMPLETE, ##< Complete / Slow mode (default)
WTMM_QUICK, ##< Quick mode 
) = range(0, 2)

# WindowTitleMatchMode
(
WTMM2_FROM_START, ##< Match the title from the start (default)
WTMM2_ANY, ##< Match any substring in the title
WTMM2_EXACT, ##< Exact title match
) = range(0, 3)

# If you want to ignore case during search window title, just mask this
# flag with option value.
WTMM2_IGNORE_CASE_FLAG = 256

__options = dict()
__options['WindowTextMatchMode'] = WTMM_COMPLETE
__options['WindowTitleMatchMode'] = WTMM2_FROM_START

def __is_title_macth(hwnd, title):
	target_title = win32gui.GetWindowText(hwnd)
	title_match_option = get_option('WindowTitleMatchMode')
	
	if title_match_option & WTMM2_IGNORE_CASE_FLAG:
		target_title = target_title.lower()
		title = title.lower()
	
	# Extrac only the option value, excluded all flags	
	title_match_option = title_match_option & 0xff
	
	if title_match_option == WTMM2_FROM_START:
		return target_title.startswith(title)
	elif title_match_option == WTMM2_ANY:
		return (title in target_title)
	elif title_match_option == WTMM2_EXACT:
		return (target_title == title)
		
	return False
	
def set_option(option_name, option_value):
	global __options
	
	if option_name not in __options:
		raise KeyError()
		
	__options[option_name] = option_value
	
	
def get_option(option_name):
	global __options
	
	if option_name not in __options:
		raise KeyError()
		
	return __options[option_name]
	
def get_list():
	windows = []
	def enum_window_callback(hwnd, extra):
		windows.append(hwnd)
		return True
	
	win32gui.EnumWindows(enum_window_callback, None)
	
	return windows
	
def exists(title=None):
	result = []
	
	if title is None:
		return True;
	
	def enum_window_callback(hwnd, result):
		if __is_title_macth(hwnd, title):
			result.append(hwnd)
			return False # Break EnumWindows() process 
		return True
	
	try:
		win32gui.EnumWindows(enum_window_callback, result)
	except pywintypes.error as e:
		if 0== e.winerror:
			# No errors, just function break from EnumWindows()
			pass
		else:
			raise e
	
	return len(result) > 0
	
def find(title=None):
	result = []
	
	if title is None:
		return True;
	
	def enum_window_callback(hwnd, result):
		if __is_title_macth(hwnd, title):
			result.append(hwnd)
			return False # Break EnumWindows() process 
		return True
	
	try:
		win32gui.EnumWindows(enum_window_callback, result)
	except pywintypes.error as e:
		if 0== e.winerror:
			# No errors, just function break from EnumWindows()
			pass
		elif 2 == e.winerror:
			# No errors, just function break from EnumWindows(), in win7 x64
			pass
		else:
			raise e
	
	if len(result) > 0:
		return result[0]
	else:
		return None
	
def wait_for(title=None, timeout=-1):
	sleep_interval = 0.1 # 100ms wake up a time. 
	counter = 0.0	
	handle = None
	while True:
		handle = find(title)
		if (handle is None) and (timeout > 0.0) and (counter > timeout):
			time.sleep(sleep_interval)
			counter += sleep_interval
		else:
			break
		
	return handle		
		
def is_valid(handle):
	return win32gui.IsWindow(handle)
