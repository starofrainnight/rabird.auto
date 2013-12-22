'''
Created on 2013-5-12

@author: "HongShe Liang <starofrainnight@gmail.com>"
'''

#--IMPORT_ALL_FROM_FUTURE--#

import time
import ctypes
import copy
import abc
import sys

class CpuTimes(object):
	def __init__(self):
		super(CpuTimes, self).__init__()
		self.wall = 0
		self.user = 0
		self.system = 0

class AbstractCpuTimer(object):
	__metaclass__ = abc.ABCMeta
	
	def __init__(self):
		super(AbstractCpuTimer, self).__init__()
		
		self.__is_stopped = True
		## Cpu times, a protected member, could be access by sub-classes
		self._cpu_times = CpuTimes()
		
	def is_stopped(self):
		return self.__is_stopped
	
	def start(self):
		self.__is_stopped = False
		self._cpu_times = CpuTimes()
	
	def stop(self):
		self.__is_stopped = True
	
	def elapsed(self):
		return copy.deepcopy(self._cpu_times)
	
	def resume(self):
		self.__is_stopped = False
	
class Win32CpuTimer(AbstractCpuTimer):
	def __init__(self):
		super(Win32CpuTimer, self).__init__()
		
		self.__old_ticks = 0
		self.__max_ticks = 0xFFFFFFFF
		
	def start(self):
		super(Win32CpuTimer, self).start()
		self.__old_ticks = win32api.GetTickCount()
		
	def elapsed(self):
		new_ticks = win32api.GetTickCount()
		delta_ticks = ( new_ticks - self.__old_ticks + self.__max_ticks ) % self.__max_ticks
		self._cpu_times.wall += ( delta_ticks / 1000.0 )
		self.__old_ticks = new_ticks
		return super(Win32CpuTimer, self).elapsed()
	
	def resume(self):
		self.__old_ticks = win32api.GetTickCount()
		super(Win32CpuTimer, self).resume()		
		
if sys.platform == 'win32' :
	import win32api
	CpuTimer = Win32CpuTimer
else:
	raise NotImplemented('The cpu_time_t not ready for unixs yet!')

##
# A class that determine if we need to sleep for a while to achieve 
# expected time.
#
# Because the python's execution is not time sensitive, if we need 
# to do something more precisely to the final expected time step 
# by step, we have to sleep to wait for current expected step time 
# or not to sleep for let the expected time catch up.
#
# This class implemented all stuffs we must care about, and provided
# a simply interface to handle the suitation. 
# 
class StepSleeper(object):
	
	def __init__(self):
		super(StepSleeper, self).__init__()
		self.__cpu_timer = CpuTimer()
		self.__final_expected_time = None
		self.__slice_time = None
		self.__next_expected_time = None
		self.__times_to_next_action= 1
		self.__times = 0
		
	def start(self, expected_time, slice_time):
		self.__final_expected_time = expected_time
		self.__next_expected_time = slice_time
		self.__slice_time = slice_time
		self.__times_to_next_action= 1
		self.__times = 0
		self.__cpu_timer.start()

	def step(self):
		self.__times += 1
		self.__next_expected_time += self.__slice_time
		if self.__times < self.__times_to_next_action:			
			return 
		
		self.__times = 0
		
		cpu_times = self.__cpu_timer.elapsed()
		if cpu_times.wall > self.__next_expected_time:
			self.__times_to_next_action += 1
			return
		
		time.sleep( self.__next_expected_time - cpu_times.wall )
		
	def stop(self):
		self.__cpu_timer.stop()
		