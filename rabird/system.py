import sys
import os

if sys.platform == "win32" :
	import rabird.windows_api

def get_single_argument_win32():
	command_line = rabird.windows_api.GetCommandLine().strip()

	script_file_name = os.path.basename(sys.argv[0])
	pos = command_line.rfind( script_file_name )
	
	result = u""
	if pos >= 0 :
		begin_index = pos + len(script_file_name) + 1
		end_index = len(command_line)
		result = command_line[begin_index:end_index].strip()
		if len(result) > 0:
			if result[0] == u"\"":
				result = result[1:len(result)-1]
	
	return result
	
def get_single_argument_others():
	result = u""
	if len(sys.argv) > 2 :
		result = sys.argv[1]
		
	return result
	
if sys.platform == "win32" :
	get_single_argument = get_single_argument_win32
else:
	get_single_argument = get_single_argument_others

