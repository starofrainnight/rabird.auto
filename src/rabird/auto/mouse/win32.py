'''
@date 2015-02-21
@author Hong-She Liang <starofrainnight@gmail.com>
'''

import win32api
import win32con
import win32gui
from . import common


class Mouse(common.Mouse):

    def __init__(self):
        super(Mouse, self).__init__()

    ##
    # send event to system
    #
    # @param event_id see win32con.MOUSEEVENTF_XXX or search in MSDN
    # @param event_data: only related to wheel event and xbutton up / down
    def send_event(self, event_id, event_data=0):
        win32api.mouse_event(event_id, 0, 0, event_data)

    # return current mouse absolute position
    def position(self):
        return win32api.GetCursorPos()

    def move(self, position):
        win32api.SetCursorPos([int(position[0]), int(position[1])])

    ##
    def button_up(self, button_type=common.ButtonType.LEFT):
        if common.ButtonType.LEFT == button_type:
            self.send_event(win32con.MOUSEEVENTF_LEFTUP)
        elif common.ButtonType.RIGHT == button_type:
            self.send_event(win32con.MOUSEEVENTF_RIGHTUP)
        elif common.ButtonType.MIDDLE == button_type:
            self.send_event(win32con.MOUSEEVENTF_MIDDLEUP)

    def button_down(self, button_type=common.ButtonType.LEFT):
        if common.ButtonType.LEFT == button_type:
            self.send_event(win32con.MOUSEEVENTF_LEFTDOWN)
        elif common.ButtonType.RIGHT == button_type:
            self.send_event(win32con.MOUSEEVENTF_RIGHTDOWN)
        elif common.ButtonType.MIDDLE == button_type:
            self.send_event(win32con.MOUSEEVENTF_MIDDLEDOWN)
