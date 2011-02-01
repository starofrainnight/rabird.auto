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
	