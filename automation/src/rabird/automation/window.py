'''
Created on 2013-8-14

@author: "HongShe Liang <starofrainnight@gmail.com>"
'''

# -*- coding: UTF-8 -*-

#--IMPORT_ALL_FROM_FUTURE--#

import win32gui
import pywintypes
import time
import locale

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

class FindContext(object):
	pass

__options = dict()
__options['WindowTextMatchMode'] = WTMM_COMPLETE
__options['WindowTitleMatchMode'] = WTMM2_FROM_START

def __is_title_macth(hwnd, title):
	target_title = win32gui.GetWindowText(hwnd).decode(locale.getpreferredencoding())
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

def __enum_windows(parent, callback, extra):
	try:
		win32gui.EnumChildWindows(parent, callback, extra)
	except pywintypes.error as e:
		if 0== e.winerror:
			# No errors, just function break from EnumChildWindows()
			pass
		elif 2 == e.winerror:
			# No errors, just function break from EnumChildWindows(), in win7 x64
			pass
		else:
			raise e

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
	
def get_list(parent=None):
	windows = []
	def enum_window_callback(hwnd, windows):
		windows.append(hwnd)
		return True
	
	__enum_windows(parent, enum_window_callback, windows)
	
	return windows
	
def exists(title=None, parent=None):
	return (find(title, parent) is not None)
	
def find(title=None, id=None, parent=None):
	result = []

	context = FindContext()
	context.result = result
	context.title = title
	context.id = id
	
	def enum_window_callback(hwnd, context):
		if context.title is not None:
			if not __is_title_macth(hwnd, context.title):
				return True
		
		if context.id is not None:
			if context.id != win32gui.GetDlgCtrlID(hwnd):
				return True
			
		context.result.append(hwnd)
		
		return False # Break EnumChildWindows() process 
	
	__enum_windows(parent, enum_window_callback, context)
	
	if len(result) > 0:
		return result[0]
	else:
		return None
	
def wait_for(title=None, timeout=-1, parent=None):
	sleep_interval = 0.1 # 100ms wake up a time. 
	counter = 0.0	
	handle = None
	while True:
		handle = find(title, parent)
		if (handle is None) and (timeout > 0.0) and (counter > timeout):
			time.sleep(sleep_interval)
			counter += sleep_interval
		else:
			break
		
	return handle	

def activate(handle):
	win32gui.SetForegroundWindow(handle)	
		
def is_valid(handle):
	return win32gui.IsWindow(handle)
