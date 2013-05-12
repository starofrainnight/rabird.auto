'''
Created on 2013-5-12

@author: "HongShe Liang <starofrainnight@gmail.com>"
'''

import win32api
import time
import ctypes

def get_elapsed_time():
	return win32api.GetTickCount() / 1000.0# GetTickCount() return seconds.

class step_timer_t(object):
	
	def __init__(self):
		super(step_timer_t, self).__init__()
		self.stop()
		
	def start(self, expected_time, slice_time):
		self.__expected_time = expected_time
		self.__slice_time = slice_time
		self.__old_time = get_elapsed_time()
		self.__next_expected_time = slice_time
		self.__times_to_next_action= 1
		self.__times = 0
	
	def step(self):
		self.__times += 1
		self.__next_expected_time += self.__slice_time
		if self.__times < self.__times_to_next_action:			
			return 
		
		self.__times = 0
		
		new_time = get_elapsed_time()
		delta_time = new_time - self.__old_time
		if delta_time > self.__next_expected_time:
			self.__times_to_next_action += 1
			return
		
		time.sleep( ( ( 0xFFFFFFFF / 1000 ) + self.__next_expected_time - delta_time ) % ( 0xFFFFFFFF / 1000 ) )
		
	def stop(self):
		self.__expected_time = None
		self.__slice_time = None
		self.__old_time = None
		self.__next_expected_time = None
		self.__times_to_next_action= 1
		self.__times = 0