'''
@author: starofrainnight
@date: 2012-3-31
'''

import exceptions

class pipe_access_error_t(exceptions.IOError):
	def __init__(self):
		super(pipe_access_error_t, self).__init__()
		
