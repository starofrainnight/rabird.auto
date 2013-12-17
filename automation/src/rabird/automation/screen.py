
#--IMPORT_ALL_FROM_FUTURE--#

'''
Created on 2013-12-17

@author: "HongShe Liang <starofrainnight@gmail.com>"
'''

import cv2
import sys
import numpy
import ImageGrab

##
# Find a specific image from screen
#
# @arg [in] target_image Target image we want to find, if input value type is 
# 'str', this method will open an image by cv2.imread(). Otherwise, the 
# target_image type should be an image stored in numpy.array.
#
# @arg [in] is_center_position If True, the result point indicate the center
# point of found image, otherwise the left-top point will be return. 
#
# @return If successed, the location of specific image on screen will 
# return, otherwise None will be return. The return position could control 
# by argument 'is_center_position'.
def find(target_image, threshold=0.7, is_center_position=True):
	match_method = cv2.TM_SQDIFF_NORMED
	screen_image = ImageGrab.grab()

	# R and B reversed !
	screen_image = numpy.array(screen_image)
	screen_image = cv2.cvtColor(screen_image, cv2.COLOR_RGB2BGR)
	
	if str==type(target_image):
		template_image = cv2.imread(target_image)
	else:
		template_image = target_image 

	result = cv2.matchTemplate(screen_image, template_image, match_method)
	min_value, max_value, min_location, max_location = cv2.minMaxLoc(result)

	# For SQDIFF and SQDIFF_NORMED, the best matches are lower values. For all the other methods, the higher the better
	if ( match_method  == cv2.TM_SQDIFF ) or ( match_method == cv2.TM_SQDIFF_NORMED ):
		match_location = min_location
		match_value = 1.0 - min_value
	else:
		match_location = max_location
		match_value = max_value
		
	if match_value < threshold:
		return None
	else:
		if is_center_position:
			match_location = (
				match_location[0] + template_image.shape[1] // 2,
				match_location[1] + template_image.shape[0] // 2 )
			
		return match_location
		
