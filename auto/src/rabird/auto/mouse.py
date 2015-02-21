# -*- coding: UTF-8 -*-

#--IMPORT_ALL_FROM_FUTURE--#

import time
import datetime
import rabird.core.datetime
import sys
from .mouse_constant import *

if sys.platform == "win32":
	from .mouse_win32 import Mouse
else:
	from .mouse_xdotool import Mouse

## move to target position 
# @param x: 
# @param y:
# @param process_time: How much seconds you want to process the whole
# mouse move operation. Default to 0.25 second
def move_to( x, y, process_time = 0.25  ):
	while 0 <= process_time  :
		start_pos = Mouse.position()
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
		timer = rabird.core.datetime.StepSleeper()
		timer.start(process_time, sleep_slice_time)
		for i in range(0,step_count):			
			temp_x += step_x
			temp_y += step_y
			Mouse.move([int(temp_x), int(temp_y)])
			timer.step()
		timer.stop()
		
		break # We must break the while!
		
	# anyway, we will move the mouse to correct position
	Mouse.move(x, y)
	time.sleep( 0.001 )

def click( button_type = ButtonType.LEFT, clicks = 1 ):
	for i in xrange(0, clicks):
		Mouse.button_down( button_type )
		time.sleep(options.click_down_delay)
		Mouse.button_up( button_type )
		time.sleep(options.click_down_delay)
