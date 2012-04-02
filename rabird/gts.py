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
import rabird.compatible
import rabird.errors
import exceptions

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

class scripter_t(rabird.compatible.unicode_t):
	__pipe_names = [
		"\\\\.\\pipe\\terminal_scripter_input",
		"\\\\.\\pipe\\terminal_scripter_output"
		]	
	
	# Command Member Index
	__CMI_ID = 0
	__CMI_NAME = 1
	__CMI_ARGUMENT = 2

	def __init__(self):
		super(scripter_t,self).__init__()
		
		self.__id = 0
		self.__pipe_handles = [0, 0]
		
		for i in xrange(0, len(self.__pipe_names)):
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
			print "Error in creating Named Pipe"
			exit()

		self.__output_pipe = self.__pipe_handles[0]
		self.__input_pipe = self.__pipe_handles[1]
		# All buffers need to split into command lines
		self.__raw_buffers = collections.deque()
		
	def connect(self, timeout = None):
		elapsed_time = 0.0
		# Wait terminal scripter connect to us.
		while 1:
			try:
				time.sleep(0.1)
				if timeout is not None:
					elapsed_time = elapsed_time + 0.1 
					if elapsed_time > timeout:
						break
				
				win32file.WriteFile(self.__output_pipe, '\n')
				# If we successed detected client connected, we break this 
				# waiting loop.
				return True
			except pywintypes.error:
				# Ignored any errors
				pass
			
		return False
	
	def __send(self, command):
		win32file.WriteFile(self.__output_pipe, '#')
		win32file.WriteFile(self.__output_pipe, command)
		win32file.WriteFile(self.__output_pipe, '\n')

	def __send_begin(self):
		result = self.__id
		
		win32file.WriteFile(self.__output_pipe, '@begin\n')
		self.__send(str(self.__id))
		self.__id = self.__id + 1
		
		return result
		
	def __send_end(self):
		win32file.WriteFile(self.__output_pipe, '@end\n')
	
	def wait_for_strings(self, strings):
		command_id = self.__send_begin()
		self.__send('wait_for_strings')
		for c in strings:
			self.__send(c)
		self.__send_end()
		command = self.__wait_for_command_with_id(command_id)
		return int(command[self.__CMI_ARGUMENT])
	
	def _quit(self):
		try:
			self.__send_begin()
			self.__send('quit')
			self.__send_end()
			
			while 1:
				time.sleep(0.1)
				try:
					# Only read could detect pipe disconnect status.
					win32file.ReadFile(self.__input_pipe, 1024)
				except pywintypes.error as e:
					if 109 == e[0]:
						raise rabird.errors.pipe_access_error_t
					elif 232 == e[0]:
						# Nothing could read from input pipe
						pass
					else:
						raise e;
		except rabird.errors.pipe_access_error_t:
			pass
		
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
			time.sleep(0.1)
			try:
				readed_size, readed_buffer = win32file.ReadFile(self.__input_pipe, 1024)
				while len(readed_buffer) > 0:
					a_line = ""
					sub_index = readed_buffer.find('\n')
					if sub_index == 0:
						if len(self.__raw_buffers) > 0:
							a_line = string.join(self.__raw_buffers)
							self.__raw_buffers.clear()
							readed_buffer = readed_buffer[(sub_index+1):len(readed_buffer)]
					elif sub_index > 0:
						sub_string = readed_buffer[0:sub_index].strip('\n\r')
						if len(sub_string) > 0:
							self.__raw_buffers.append(sub_string)
							
						if len(self.__raw_buffers) > 0:
							a_line = string.join(self.__raw_buffers)
							
						self.__raw_buffers.clear()
						readed_buffer = readed_buffer[(sub_index+1):len(readed_buffer)]
					else:
						sub_string = readed_buffer.strip('\n\r')
						if len(sub_string) > 0:
							self.__raw_buffers.append(sub_string)
						break
					
					if len(a_line) > 0:
						if cmp(a_line, "@begin") == 0:
							a_command = []
						elif cmp(a_line, "@end") == 0:
							if a_command is not None:
								return a_command
						elif a_command is not None:
							# Remove prefix "#" and append to command
							a_command.append(a_line[1:len(a_line)]) 
			except pywintypes.error as e:
				if 109 == e[0]:
					raise rabird.errors.pipe_access_error_t
				elif 232 == e[0]:
					# Nothing could read from input pipe
					pass
				else:
					raise e

	def __wait_for_command_with_id(self, command_id):
		while 1:
			command = self.__wait_for_command()
			
			# A command at least have two element : ID, Command Name 
			if len(command) < 2:
				continue
			
			if 0 == cmp(str(command_id), command[self.__CMI_ID]):
				return command
				
				
