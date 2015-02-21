'''
@date 2015-02-21
@author Hong-She Liang <starofrainnight@gmail.com>
'''

from rabird.core.enum import Enum 

# button types
class ButtonType(Enum):
    LEFT = 0
    MIDDLE = 1
    RIGHT = 2

# button status
class ButtonStatus(Enum):
    UP = 0
    DOWN = 1

## all time related unit are second, see description about sleep() function 
# of module time.
class ButtonOptions():
    click_delay = 0.010
    click_down_delay = 0.010
    click_drag_delay = 0.250

## options of mouse related functions
options = ButtonOptions()

