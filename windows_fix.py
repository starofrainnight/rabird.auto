##
# import this unit to fixed multilanguage read /write problems, 
# it's a rarely appear problem : even you set the correct locale, 
# if there are a folder / file name is mix with different language copy 
# from other windows PC, you could not read / write with the correct 
# name !
# 
# we have to do many jobs to fix it :
# 
# 1. replace the stdout / stderr / stdin file object in sys with our fixed objects
# 2. fixed the sys.argv list with GetCommandLine() api in win32 
# 3. fixed os.path series problems 
# 4. may be there have more we have not found yet! ...
#
# @date 2011-1-25
# @author: HongShe Liang <starofrainnight@gmail.com>
#  
import sys
import os
import io
import threading
import atexit 
import win32console 
import win32api
import types # for all standard type values for buildin type()
import pickle
import rabird.windows_api
import time

# * replace the stdout / stderr / stdin file object in sys with our fixed objects

class stdout_thread_t(threading.Thread):
	def __init__(self, file_descriptor, std_handle_type, old_stdout):
		threading.Thread.__init__(self)
		# so that if the main thread exit, our thread will also exit
		self.setDaemon(True)
		self.file_descriptor = file_descriptor
		self.std_handle_type = std_handle_type
		self.old_stdout = old_stdout
		
		# use for internal purpose 
		self.screen_buffer = win32console.GetStdHandle(self.std_handle_type)
		# do not open the file in text mode, otherwise it will try to decode
		# with the encoding, but the unicode sometimes included something 
		# do not in the encoding scale, that will case a convertion error:
		# 'ascii' codec can't encode character u'\xbb' in position ...
		self.stdout = io.open(self.file_descriptor, mode='rb')
		
	def run(self):
		end_mark = ord(".")
		exit_mark = ord("@")

		while True:
			# it will be block here until any string coming ...
			# we shoudl be read three lines for a unit ( the pickle format )
			temp_line = ""
			a_line = ""
			
			while True:
				temp_line = self.stdout.readline()				
				a_line += temp_line
				
				if len(temp_line) > 0:
					if ord(temp_line[0]) == end_mark:
						break
				
			# if outside need us to destroy our self, we exit ...
			if len(temp_line) >= 2:
				if ord(temp_line[1]) == exit_mark:
					break

			if not a_line :
				continue
				
			s = pickle.loads(a_line)
			if len(s) <= 0 :
				continue
				
			if(type(s) == types.UnicodeType) :
				self.screen_buffer.WriteConsole(s)
			else :
				self.old_stdout.write(s)		
		
class stdio_file_t(io.FileIO): 
	def __init__(self, name, mode='r', closefd=True):
		io.FileIO.__init__(self, name, mode, closefd) 

	def write(self, value):
		if(type(value) != types.UnicodeType) :
			value = str(value) # changed value to str 
			
		# the line separator must be at the end of line !
		value = str(pickle.dumps(value)) + os.linesep
		io.FileIO.write(self, value)		
		
		
def stop_stdout_thread( a_thread, a_stdout_file ):
	os.write( a_stdout_file.fileno(), ".@\n" ) # break the read line operation in thread
	a_thread.join()

stdout_pipe = os.pipe()
stderr_pipe = os.pipe()
stdin_pipe = os.pipe()

old_stdout = sys.stdout
old_stderr = sys.stderr
old_stdin = sys.stdin

stdout_thread = stdout_thread_t(stdout_pipe[0], win32api.STD_OUTPUT_HANDLE, old_stdout)
stderr_thread = stdout_thread_t(stderr_pipe[0], win32api.STD_ERROR_HANDLE, old_stderr)

stdout_thread.start()
stderr_thread.start()

# to test our stdout with new stdout
our_stdout = stdio_file_t(stdout_pipe[1], "wb")
our_stderr = stdio_file_t(stderr_pipe[1], "wb")

sys.stdout = our_stdout
# keep not to overwrite the sys.stderr for debug purpose
sys.stderr = our_stderr

# * fixed the sys.argv list with GetCommandLine() api in win32
sys.argv = rabird.windows_api.CommandLineToArgv(rabird.windows_api.GetCommandLine())

# * finalize windows's unicode fix
def __on_exit_rabird_module():
	# wait for console finished their output
	stop_stdout_thread( stdout_thread, our_stdout )
	stop_stdout_thread( stderr_thread, our_stderr )
	
	# restore original standard input/output 
	sys.stderr = old_stderr
	sys.stdout = old_stdout
	sys.stdin = old_stdin

	# close all pipes	
	for i in stdin_pipe:
		os.close(i)

# we must restore original standard input/output file
atexit.register(__on_exit_rabird_module)

