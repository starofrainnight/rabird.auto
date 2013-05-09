
#--IMPORT_ALL_FROM_FUTURE--#

import time
import win32pipe
import win32file
import pywintypes
import collections
import string
import rabird.gts
import sys
import logging

scripter = rabird.gts.create_scripter('securecrt')

logging.info("Wating connection ...")

scripter.connect()

logging.info("Execute commands ...")

try:
	scripter.send('echo hello\n')
	result = scripter.wait_for_strings(['hello'])
	logging.info( 'result : ' + str(result) ) 
	scripter.send_keys('{NUM_9}')
	scripter.send_keys('{NUM_ENTER}')
	scripter._quit()
except ConnectionAbortedError:
	pass

logging.info("Exit ...")

