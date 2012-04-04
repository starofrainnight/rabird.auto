'''
@author: starofrainnight
@date: 2012-3-31
'''

import exceptions

class timeout_warning_t(exceptions.RuntimeWarning):
	def __init__(self):
		super(timeout_warning_t, self).__init__()


