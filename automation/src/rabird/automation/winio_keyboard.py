'''
Created on 2013-12-14

@author: "HongShe Liang <starofrainnight@gmail.com>"
'''

import pywinio
import time
import win32api
import win32con
import atexit

# KeyBoarD Commands
# Command port
KBC_KEY_CMD	= 0x64
# Data port
KBC_KEY_DATA = 0x60

winio = pywinio.WinIO()

def __set_winio_to_none():
	global winio
	winio = None
	
atexit.register(__set_winio_to_none)

# Wait keyboard buffer empty
def wait_for_buffer_empty():
	global winio
	
	dwRegVal = 0x02
	while (dwRegVal & 0x02):
		dwRegVal = winio.get_port_byte(KBC_KEY_CMD)
		
def key_down(scancode):
	global winio
	
	wait_for_buffer_empty();
	winio.set_port_byte(KBC_KEY_CMD, 0xd2);
	wait_for_buffer_empty();
	winio.set_port_byte(KBC_KEY_DATA, scancode)

def key_up(scancode):
	global winio
	
	wait_for_buffer_empty();
	winio.set_port_byte( KBC_KEY_CMD, 0xd2);
	wait_for_buffer_empty();
	winio.set_port_byte( KBC_KEY_DATA, scancode | 0x80);

def key_press(scancode, press_time = 0.2):
	key_down( scancode )
	time.sleep( press_time )
	key_up( scancode )

def keybd_event(vkcode, scancode, flags):
	extend_code = ( scancode >> 8 ) & 0xff
	standard_code = scancode & 0xff
	is_key_up = ((flags & win32con.KEYEVENTF_KEYUP) > 0)
	
	if extend_code > 0:
		if is_key_up:
			key_up(extend_code)
		else:
			key_down(extend_code)
	
	if is_key_up:
		key_up(standard_code)
	else:
		key_down(standard_code)
