##
# A compatile support module for 2.x and 3.x .
# 
# Some ideas came from Armin Ronacher. References to 
# http://lucumr.pocoo.org/2011/1/22/forwards-compatible-python/.
#
# There have another Python 2 and 3 compatibility utilities module named 'six'
# takes a great deal jobs, you have better use it to write your applications. 
# References to http://pypi.python.org/pypi/six/.
#
# @date 2011-11-13
# @author: starofrainnight
import sys

##
# Unicode support for __str__() and __unicode__(). 
# 
# In 2.x version, we implement a __str__() by encode to utf-8 format from 
# __unicode__().
# 
# In 3.x version, the __unicode__() is unused, so we implement the __str__() by 
# directly invoke __unicode__().
# 
# What that means ? That means we only need to implement the __unicode__(), and
# all other jobs will be done by class unicode_t.
# 
# You just need to do is inherit from it.
class unicode_t(object):
	if sys.version_info.major >= 3:
		__str__ = lambda x: x.__unicode__()
	else:
		__str__ = lambda x: unicode(x).encode('utf-8')
