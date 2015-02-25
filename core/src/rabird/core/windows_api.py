


##
# pywin32 actially do not support unicode version of windows api, just as if 
# you input the multilanguage ( mix different language characters ). for ex:
# the api GetCommandLine() will return a string object decoded by current locale,
# if all the characters are in the scale of locale, that's fine, it will no 
# harm to the program, but if there have some characters if no in the scale of 
# locale, and in the unicode scale, it's covertion will broken the finally 
# string. 
#
# so we have to use our "W" version apis ( unicode version apis ) to finish our
# job.  
# 
import ctypes

# @return an unicode string indicate the command line
def GetCommandLine():	
	return ctypes.c_wchar_p( ctypes.windll.kernel32.GetCommandLineW() ).value

def CommandLineToArgv( ACommandLine  ):
	arguments_count = ctypes.c_int()
	arguments_memory = ctypes.c_void_p( ctypes.windll.shell32.CommandLineToArgvW( ctypes.c_wchar_p(ACommandLine), ctypes.byref(arguments_count) ) )
	
	result = []		
	if 0 != arguments_memory.value :
		for i in xrange( 1, arguments_count.value ):
			wstring_memory = ctypes.c_void_p.from_address( arguments_memory.value + i * ctypes.sizeof(ctypes.c_void_p) )
			result.append( ctypes.wstring_at( wstring_memory.value ) )

	ctypes.windll.kernel32.LocalFree( arguments_memory )
	
	return result
	
def IsUserAnAdmin():
	import ctypes
	# WARNING: requires Windows XP SP2 or higher!
	try:
		return ctypes.windll.shell32.IsUserAnAdmin()
	except:
		traceback.print_exc()
		return False

def RunAsAdmin(command_line=None, wait=True):
	import win32api
	import win32con
	import win32event
	import win32process
	from win32com.shell.shell import ShellExecuteEx
	from win32com.shell import shellcon

	python_exe = sys.executable

	if command_line is None:
		command_line = [python_exe] + sys.argv
	elif type(command_line) not in (types.TupleType, types.ListType):
		raise ValueError, "command_line is not a sequence."
	cmd = '"%s"' % (command_line[0],)
	# XXX TODO: isn't there a function or something we can call to massage command line params?
	params = " ".join(['"%s"' % (x,) for x in command_line[1:]])
	command_dir = ''
	show_command = win32con.SW_SHOWNORMAL
	#show_command = win32con.SW_HIDE
	lpVerb = 'runas'  # causes UAC elevation prompt.

	# print "Running", cmd, params

	# ShellExecute() doesn't seem to allow us to fetch the PID or handle
	# of the process, so we can't get anything useful from it. Therefore
	# the more complex ShellExecuteEx() must be used.

	# handle = win32api.ShellExecute(0, lpVerb, cmd, params, command_dir, show_command)

	process_info = ShellExecuteEx(nShow=show_command,
							  fMask=shellcon.SEE_MASK_NOCLOSEPROCESS,
							  lpVerb=lpVerb,
							  lpFile=cmd,
							  lpParameters=params)

	if wait:
		handle = process_info['hProcess']	
		obj = win32event.WaitForSingleObject(handle, win32event.INFINITE)
		rc = win32process.GetExitCodeProcess(handle)
	else:
		rc = None

	return rc	