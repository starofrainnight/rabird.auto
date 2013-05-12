# -*- coding: UTF-8 -*-

#--IMPORT_ALL_FROM_FUTURE--#

import win32api, win32con, win32gui
import time
import datetime
import rabird.datetime

# button types
BT_LEFT = 0
BT_MIDDLE = 1
BT_RIGHT = 2

# button status
BS_UP = 0
BS_DOWN = 1

## all time related unit are second, see description about sleep() function 
# of module time.
class mouse_options_t():
	click_delay = 0.010
	click_down_delay = 0.010
	click_drag_delay = 0.250

## options of mouse related functions
options = mouse_options_t()

##
# send event to system 
#
# @param event_id see win32con.MOUSEEVENTF_XXX or search in MSDN
# @param event_data: only related to wheel event and xbutton up / down 
def send_event( event_id, event_data = 0 ):
	win32api.mouse_event( event_id, 0, 0, event_data )

## return current mouse absolute position
def position():
	return win32api.GetCursorPos()

## move to target position 
# @param x: 
# @param y:
# @param process_time: How much seconds you want to process the whole
# mouse move operation. Default to 0.25 second
def move_to( x, y, process_time = 0.25  ):
	while 0 <= process_time  :
		start_pos = position()
		start_x = start_pos[0]
		start_y = start_pos[1]
		
		if start_x < x:
			symbol_x = 1
		else:
			symbol_x = -1
			
		if start_y < y:
			symbol_y = 1
		else:
			symbol_y = -1
			
		distance_x = abs( x - start_x )
		distance_y = abs( y - start_y )
		
		if distance_x > distance_y:
			if 0 == distance_y:
				step_x = float(distance_x)
				step_y = 0
				step_count = int(distance_x)
			else:
				step_x = float(distance_x) / distance_y 
				step_y = float(1.0)
				step_count = int(distance_y)
		else:
			if 0 == distance_x:
				step_x = 0
				step_y = float(distance_y)
				step_count = int(distance_y)
			else:
				step_x = float(1.0)
				step_y = float(distance_y) / distance_x
				step_count = int(distance_x)
			
		step_x = symbol_x * step_x
		step_y = symbol_y * step_y
		
		temp_x = start_x
		temp_y = start_y
		
		# The step count too small, just one step enough!
		if step_count <= 1:
			break
		
		sleep_slice_time = process_time / step_count
		timer = rabird.datetime.step_timer_t()
		timer.start(process_time, sleep_slice_time)
		for i in range(0,step_count):			
			temp_x += step_x
			temp_y += step_y
			win32api.SetCursorPos( [int(temp_x), int(temp_y)] )
			timer.step()
		timer.stop()
		
		break # We must break the while!
		
	# anyway, we will move the mouse to correct position
	win32api.SetCursorPos( [x, y] )
	time.sleep( 0.001 )

##  
def button_up( button_type = BT_LEFT ):
	if BT_LEFT == button_type:
		send_event( win32con.MOUSEEVENTF_LEFTUP )
	elif BT_RIGHT == button_type:
		send_event( win32con.MOUSEEVENTF_RIGHTUP )
	elif BT_MIDDLE == button_type:
		send_event( win32con.MOUSEEVENTF_MIDDLEUP )
		
def button_down( button_type = BT_LEFT ):
	if BT_LEFT == button_type:
		send_event( win32con.MOUSEEVENTF_LEFTDOWN )
	elif BT_RIGHT == button_type:
		send_event( win32con.MOUSEEVENTF_RIGHTDOWN )
	elif BT_MIDDLE == button_type:
		send_event( win32con.MOUSEEVENTF_MIDDLEDOWN )
		
def click( button_type = BT_LEFT ):
	button_down( button_type )
	time.sleep( options.click_down_delay )
	button_up( button_type )
	
def double_click( button_type = BT_LEFT ):
	click( button_type )
	# we read the double click time in real time, because the value will be
	# changed by user . we must keep the double click time less than the real
	# double click time ( plus script running time ), so we divide the system
	# double click time to a half.
	time.sleep( float(win32gui.GetDoubleClickTime()) / 2000 )
	click( button_type )
