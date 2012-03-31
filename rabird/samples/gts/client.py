
import time
import win32pipe
import win32file
import pywintypes
import collections
import string
import rabird.gts
import rabird.errors
import exceptions
import sys

scripter = rabird.gts.scripter_t()

print "Wating connection ..."

scripter.wait_for_connection()

print "Execute commands ..."

try:
	result = scripter.wait_for_strings(['hello'])
	print 'result : ' + str(result) 
	scripter.remote_quit()
except rabird.errors.pipe_access_error_t:
	pass

print "Exit ..."

