#!/usr/bin/python
# -*- coding: UTF-8 -*-
import win32api, win32con, win32gui
import time

def position():
	return win32api.GetCursorPos()

def move_to( x, y, is_smooth = False, speed = 0.001 ):
	if is_smooth :
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
		
		for i in xrange(0,step_count):			
			temp_x += step_x
			temp_y += step_y
			win32api.SetCursorPos( [int(temp_x), int(temp_y)] )
			time.sleep( speed )
			
	# anyway, we will move the mouse to correct position
	win32api.SetCursorPos( [x, y] )

