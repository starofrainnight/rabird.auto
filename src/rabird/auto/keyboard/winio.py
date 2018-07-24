'''
@date 2013-12-14
@author Hong-She Liang <starofrainnight@gmail.com>
'''

import pywinio
import time
import win32api
import win32con
import atexit

# KeyBoarD Commands
# Command port
KBC_KEY_CMD = 0x64
# Data port
KBC_KEY_DATA = 0x60

__winio = None


def __get_winio():
    global __winio

    if __winio is None:
        __winio = pywinio.WinIO()

        def __clear_winio():
            global __winio
            __winio = None
        atexit.register(__clear_winio)

    return __winio


def wait_for_buffer_empty():
    '''
    Wait keyboard buffer empty
    '''

    winio = __get_winio()

    dwRegVal = 0x02
    while (dwRegVal & 0x02):
        dwRegVal = winio.get_port_byte(KBC_KEY_CMD)


def key_down(scancode):
    winio = __get_winio()

    wait_for_buffer_empty()
    winio.set_port_byte(KBC_KEY_CMD, 0xd2)
    wait_for_buffer_empty()
    winio.set_port_byte(KBC_KEY_DATA, scancode)


def key_up(scancode):
    winio = __get_winio()

    wait_for_buffer_empty()
    winio.set_port_byte(KBC_KEY_CMD, 0xd2)
    wait_for_buffer_empty()
    winio.set_port_byte(KBC_KEY_DATA, scancode | 0x80)


def key_press(scancode, press_time=0.2):
    key_down(scancode)
    time.sleep(press_time)
    key_up(scancode)


def keybd_event(vkcode, scancode, flags):
    extend_code = (scancode >> 8)
    standard_code = scancode & 0xff
    is_key_up = ((flags & win32con.KEYEVENTF_KEYUP) > 0)

    if extend_code > 0:
        is_found_value = False
        for shiftbits in range(56, 0, -8):
            extend_code = (scancode >> shiftbits) & 0xff

            if not is_found_value:
                if extend_code == 0:
                    continue
                else:
                    is_found_value = True

            # Extend code must not mark with 0x80 (key up behavior)
            key_down(extend_code)

    if is_key_up:
        key_up(standard_code)
    else:
        key_down(standard_code)
