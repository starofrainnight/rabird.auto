import sys
import os
import io
import threading
import time
import atexit  

stdout_pipe = os.pipe();
stderr_pipe = os.pipe();
stdin_pipe = os.pipe();

class stdout_thread_t(threading.Thread):
    def __init__(self, file_descriptor ):
        threading.Thread.__init__(self)
        # so that if the main thread exit, our thread will also exit
        self.setDaemon(True)
        self.file_descriptor = file_descriptor

    def run(self):
		try :
			while True:
				print "test"
				# it will be block here until any string coming ...
				s = os.read(self.file_descriptor, 256)
				print "s = " + s
		except :
			print "ok, we finished our thread ... "
			pass
    			
stdout_thread = stdout_thread_t( stdout_pipe[0] )
stderr_thread = stdout_thread_t( stderr_pipe[0] )

stdout_thread.start()
stderr_thread.start()


def __on_exit_rabird_module():
	pass

atexit.register( __on_exit_rabird_module )