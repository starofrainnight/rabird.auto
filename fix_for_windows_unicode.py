#
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
import cPickle as pickle

stdout_pipe = os.pipe()
stderr_pipe = os.pipe()
stdin_pipe = os.pipe()

old_stdout = sys.stdout
old_stderr = sys.stderr
old_stdin = sys.stdin

class stdout_thread_t(threading.Thread):
    def __init__(self, file_descriptor, std_handle_type ):
        threading.Thread.__init__(self)
        # so that if the main thread exit, our thread will also exit
        self.setDaemon(True)
        self.file_descriptor = file_descriptor
        self.std_handle_type = std_handle_type

    def run(self):
		screen_buffer = win32console.GetStdHandle( self.std_handle_type )

		# do not open the file in text mode, otherwise it will try to decode
		# with the encoding, but the unicode sometimes included something 
		# do not in the encoding scale, that will case a convertion error:
		# 'ascii' codec can't encode character u'\xbb' in position ...
		stdout_file = io.open(self.file_descriptor, mode='rb', closefd=False)

		while True:
			# it will be block here until any string coming ...
			s = pickle.load(stdout_file)	
			if len(s) > 0 :
				if( type(s) == types.UnicodeType ) :
					screen_buffer.WriteConsole( s )
				else :
					old_stdout.write( s )
				
class stdio_file_t( io.FileIO ): 
	def __init__(self, name, mode='r', closefd=True):
		io.FileIO.__init__(self, name, mode, closefd ) 

	def write(self, value ):
		if( type(value) != types.UnicodeType ) :
			value = str(value) # changed value to str 

		io.FileIO.write( self, pickle.dumps( value ) )		

stdout_thread = stdout_thread_t( stdout_pipe[0], win32api.STD_OUTPUT_HANDLE )
stderr_thread = stdout_thread_t( stderr_pipe[0], win32api.STD_ERROR_HANDLE )

stdout_thread.start()
stderr_thread.start()

# to test our stdout with new stdout
sys.stdout = stdio_file_t( stdout_pipe[1], "wb", closefd=False )
# keep not to overwrite the sys.stderr for debug purpose
sys.stderr = stdio_file_t( stderr_pipe[1], "wb", closefd=False )

def __on_exit_rabird_module():
	# restore original standard input/output 
	sys.stderr = old_stderr
	sys.stdout = old_stdout
	sys.stdin = old_stdin
	
	# FIXME : when we want to close the handles open by pipe(), it seems that
	# the script just blocked down , thought it's no harm to no close the 
	# handles, but it's really confuse me...

# we must restore original standard input/output file
atexit.register( __on_exit_rabird_module )

