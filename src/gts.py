
#--IMPORT_ALL_FROM_FUTURE--#

'''
GTS ( General Terminal Scripter ) .

Only supported in windows.

@author: starofrainnight
@date: 2012-3-30
'''

import time
import win32pipe
import win32file
import pywintypes
import collections
import string
import abc
import win32gui
import logging
import six
from . import compatible

PIPE_ACCESS_DUPLEX = 0x3
PIPE_TYPE_MESSAGE = 0x4
PIPE_READMODE_MESSAGE = 0x2
PIPE_WAIT = 0
PIPE_NOWAIT = 1
PIPE_UNLIMITED_INSTANCES = 255
BUFSIZE = 4096
NMPWAIT_USE_DEFAULT_WAIT = 0
INVALID_HANDLE_VALUE = -1
ERROR_PIPE_CONNECTED = 535

class scripter_t(compatible.unicode_t):
	__metaclass__ = abc.ABCMeta

	# Command Member Index
	__CMI_ID = 0
	__CMI_NAME = 1
	__CMI_ARGUMENT = 2
	
	def __init__(self, *args, **kwarg):
		super(scripter_t,self).__init__()
		
		self.__pipe_names = [
			"\\\\.\\pipe\\terminal_scripter_input",
			"\\\\.\\pipe\\terminal_scripter_output"
			]
			
		self.__id = 0
		self.__pipe_handles = [0, 0]
		
		for i in range(0, len(self.__pipe_names)):
			self.__pipe_handles[i] = win32pipe.CreateNamedPipe(
				self.__pipe_names[i],
				PIPE_ACCESS_DUPLEX,
				PIPE_TYPE_MESSAGE |	PIPE_READMODE_MESSAGE |	PIPE_NOWAIT,
				PIPE_UNLIMITED_INSTANCES,
				BUFSIZE, BUFSIZE,
				NMPWAIT_USE_DEFAULT_WAIT,
				None
				)
	
		if not self.__pipe_handles[i]:
			logging.error("Error while in creating Named Pipe")
			exit()

		self.__output_pipe = self.__pipe_handles[0]
		self.__input_pipe = self.__pipe_handles[1]
		# All buffers need to split into command lines
		self.__raw_buffers = collections.deque()
		
	def _send(self, command):
		win32file.WriteFile(self.__output_pipe, b'#')
		win32file.WriteFile(self.__output_pipe, six.b(command))
		win32file.WriteFile(self.__output_pipe, b'\n')

	def _send_begin(self):
		result = self.__id
		
		win32file.WriteFile(self.__output_pipe, b'@begin\n')
		self._send(str(self.__id))
		self.__id = self.__id + 1
		
		return result
		
	def _send_end(self):
		win32file.WriteFile(self.__output_pipe, b'@end\n')
	
	##
	#
	# Wait for a command
	#
	# @return:  If successed, a new command will be returned. If pipe be disconnected, 
	# a None will be returned.
	def __wait_for_command(self):
		readed_size = 0
		readed_buffer = "" 
		a_line = ""
		a_command = None
		sub_index = 0
		while 1:
			try:
				readed_size, readed_buffer = win32file.ReadFile(self.__input_pipe, 1024)
				while len(readed_buffer) > 0:
					a_line = ""
					sub_index = readed_buffer.find(b'\n')
					if sub_index == 0:
						if len(self.__raw_buffers) > 0:
							a_line = b''.join(self.__raw_buffers)
							self.__raw_buffers.clear()
							readed_buffer = readed_buffer[(sub_index+1):len(readed_buffer)]
					elif sub_index > 0:
						sub_string = readed_buffer[0:sub_index].strip(b'\n\r')
						if len(sub_string) > 0:
							self.__raw_buffers.append(sub_string)
							
						if len(self.__raw_buffers) > 0:
							a_line = b''.join(self.__raw_buffers)
							
						self.__raw_buffers.clear()
						readed_buffer = readed_buffer[(sub_index+1):len(readed_buffer)]
					else:
						sub_string = readed_buffer.strip(b'\n\r')
						if len(sub_string) > 0:
							self.__raw_buffers.append(sub_string)
						break
					
					if len(a_line) > 0:
						if a_line == b"@begin":
							a_command = []
						elif a_line == b"@end":
							if a_command is not None:
								return a_command
						elif a_command is not None:
							# Remove prefix "#" and append to command
							a_command.append(a_line[1:len(a_line)]) 
			except pywintypes.error as e:
				if 109 == e.winerror:
					raise ConnectionAbortedError()
				elif 232 == e.winerror:
					# Nothing could read from input pipe
					time.sleep(0.1)
					pass
				else:
					raise e

	def __wait_for_command_with_id(self, command_id):
		while 1:
			command = self.__wait_for_command()
			
			# A command at least have two element : ID, Command Name 
			if len(command) < 2:
				continue
			
			if int(command_id) == int(command[self.__CMI_ID]):
				return command
			
	def connect(self, timeout=None):
		elapsed_time = 0.0
		# Wait terminal scripter connect to us.
		while 1:
			try:
				time.sleep(0.1)
				if timeout is not None:
					elapsed_time = elapsed_time + 0.1 
					if elapsed_time > timeout:
						break
				
				win32file.WriteFile(self.__output_pipe, b'\n')
				# If we successed detected client connected, we break this 
				# waiting loop.
				return True
			except pywintypes.error:
				# Ignored any errors
				pass
			
		return False
	
	def _execute(self, command):
		command_id = self._send_begin()
		self._send('execute')
		self._send(command)
		self._send_end()
		command = self.__wait_for_command_with_id(command_id)

	def _get_value(self, command):
		command_id = self._send_begin()
		self._send('get_value')
		self._send(command)
		self._send_end()
		command = self.__wait_for_command_with_id(command_id)
		return command[self.__CMI_ARGUMENT]
	
	@abc.abstractmethod
	def wait_for_strings(self, strings):
		pass
	
	@abc.abstractmethod
	def send(self, input_string):
		pass
	
	@abc.abstractmethod
	def send_keys(self, input_string):
		pass

	@abc.abstractmethod
	def _do_quit(self, error_code):
		pass
		
	def _quit(self, error_code=0):
		try:
			self._do_quit(error_code)
			
			while 1:
				try:
					# Only read could detect pipe disconnect status.
					win32file.ReadFile(self.__input_pipe, 1024)
				except pywintypes.error as e:
					if 109 == e.winerror:
						raise ConnectionAbortedError
					elif 232 == e.winerror:
						# Nothing could read from input pipe
						time.sleep(0.1)
					else:
						raise e;
		except ConnectionAbortedError:
			pass

class securecrt_scripter_t(scripter_t):
	
	def __escape_string(self, astring):
		escaped_chars = []
		
		for c in astring:
			if len(escaped_chars) > 0:
				escaped_chars.append('&')
				
			escaped_chars.append('chr(' + str(ord(c)) + ')')
			
		return ''.join(escaped_chars)
		
	def wait_for_strings(self, strings):
		escaped_strings = []
		
		for s in strings:
			escaped_strings.append(self.__escape_string(s))
			
		command = 'result = crt.screen.WaitForStrings(' + ','.join(escaped_strings) + ')'
				
		self._execute(command)
		return int(self._get_value('result')) - 1
	
	def send(self, input_string):
		self._execute('crt.screen.Send ' + self.__escape_string(input_string))
	
	def send_keys(self, input_string):
		self._execute('crt.screen.SendKeys "' + input_string + '"')

	def _do_quit(self, error_code):
		# WScript.Quit may not existed before v6.7 
		# self._execute("WScript.Quit " + str(error_code))
		self._send_begin()
		self._send('quit')
		self._send_end()
		
class teraterm_scripter_t(scripter_t):
	
	def __init__(self, *args, **kwarg):
		super(teraterm_scripter_t, self).__init__(self, *args, **kwarg)
		
		self.__target_window = None
	
	def __escape_string(self, astring):
		escaped_chars = []
		
		for c in astring:
			escaped_chars.append('#' + str(ord(c)))
			
		return ''.join(escaped_chars)
	
	def connect(self, timeout=None):
		super(teraterm_scripter_t, self).connect(self)

		# Get old title of teraterm		
		self._execute('gettitle __old_title')
		old_title = self._get_value('__old_title')
		
		# Set the teraterm window title to "rabird_gts_target_window"
		self._execute('settitle "rabird_gts_target_window"')
		
		# Find the teraterm window 
		window = 0
		while 1:
			window = win32gui.FindWindowEx(
				0, 
				window, 
				'VTWin32', 
				None )
			
			if not window:
				break
			
			if win32gui.GetWindowText(window).find('rabird_gts_target_window') >= 0 :
				self.__target_window = window
				break
			
		# Restore title
		self._execute('settitle "' + old_title + '"')
			
	def wait_for_strings(self, strings):
		escaped_strings = []
		
		for s in strings:
			escaped_strings.append(self.__escape_string(s))
			
		self._execute('wait ' + ''.join(escaped_strings))
		self._execute('int2str __last_command_result_str __last_command_result') 
		
		return int(self._get_value('__last_command_result_str')) - 1
	
	def send(self, input_string):
		self._execute('send ' + self.__escape_string(input_string))
	
	def send_keys(self, input_string):
		pass

	def _do_quit(self, error_code):
		self._send_begin()
		self._send('quit')
		self._send_end()
		

def create_scripter(name):
	if 'securecrt' == name:
		return securecrt_scripter_t()
	elif 'teraterm' == name:
		return teraterm_scripter_t()
	else:
		raise NotImplemented('Unknow scripter : {}'.format(name))