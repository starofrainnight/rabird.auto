#
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

def GetCommandLine():	
	result = ctypes.c_wchar_p( ctypes.windll.kernel32.GetCommandLineW() )
	print result	 
