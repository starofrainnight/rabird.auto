
#--IMPORT_ALL_FROM_FUTURE--#

import time
import win32pipe
import win32file
import pywintypes
import collections
import string
import rabird.gts
import sys
import os
import logging

if 'PYTHON_LOGGING_LEVEL' in os.environ:
	try:
		logging.basicConfig(level=logging.getLevelName(os.environ['PYTHON_LOGGING_LEVEL']))
	except ValueError:
		pass

# It would exit the script if user use a scripter we have not support yet.
scripter = rabird.gts.create_scripter('securecrt')

logging.info("Wating connection ...")

scripter.connect()

logging.info("Execute commands ...")

try:
	scripter.send('echo hello\n')
	result = scripter.wait_for_strings(['hello'])
	scripter.send_keys('{NUM_9}')
	scripter.send_keys('{NUM_ENTER}')
	scripter._quit()
except ConnectionAbortedError:
	pass

logging.info("Exit ...")

