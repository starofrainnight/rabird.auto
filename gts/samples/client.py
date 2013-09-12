
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
import rabird.logging

def usage():
	print('{} [scripter name]'.format(__file__))

def main():
	rabird.logging.load_default_config()
	if len(sys.argv)<2:
		usage()
		return -1
		
	# It would exit the script if user use a scripter we have not support yet.
	scripter = rabird.gts.create_scripter(sys.argv[1])
	
	logging.info("Waiting connection ...")
	
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

if __name__ == "__main__":
	exit(main())
