'''
@date 2015-02-21
@author Hong-She Liang <starofrainnight@gmail.com>
'''

import time
import datetime
import sys
import rabird.core.datetime
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

class Mouse(object):
    def __init__(self):
        pass
    
        
    ## move to target position 
    # @param x: 
    # @param y:
    # @param process_time: How much seconds you want to process the whole
    # mouse move operation. Default to 0.25 second
    def move(self, position, process_time = 0.25  ):
        x = position[0]
        y = position[1]
        
        while 0 <= process_time  :
            start_pos = self.position()
            start_x = start_pos[0]
            start_y = start_pos[1]
            
            if start_x < x:
                symbol_x = 1
            else:
                symbol_x = -1
                
            if start_y < y:
                symbol_y = 1
            else:
                symbol_y = -1
                
            distance_x = abs( x - start_x )
            distance_y = abs( y - start_y )
            
            if distance_x > distance_y:
                if 0 == distance_y:
                    step_x = float(distance_x)
                    step_y = 0
                    step_count = int(distance_x)
                else:
                    step_x = float(distance_x) / distance_y 
                    step_y = float(1.0)
                    step_count = int(distance_y)
            else:
                if 0 == distance_x:
                    step_x = 0
                    step_y = float(distance_y)
                    step_count = int(distance_y)
                else:
                    step_x = float(1.0)
                    step_y = float(distance_y) / distance_x
                    step_count = int(distance_x)
                
            step_x = symbol_x * step_x
            step_y = symbol_y * step_y
            
            temp_x = start_x
            temp_y = start_y
            
            # The step count too small, just one step enough!
            if step_count <= 1:
                break
            
            sleep_slice_time = process_time / step_count
            timer = rabird.core.datetime.StepSleeper()
            timer.start(process_time, sleep_slice_time)
            for i in range(0,step_count):            
                temp_x += step_x
                temp_y += step_y
                self.move([int(temp_x), int(temp_y)])
                timer.step()
            timer.stop()
            
            break # We must break the while!
            
        # anyway, we will move the mouse to correct position
        self.move(position)
        time.sleep( 0.001 )
    
    def click(self, button_type = ButtonType.LEFT, clicks = 1 ):
        for i in xrange(0, clicks):
            self.button_down( button_type )
            time.sleep(options.click_down_delay)
            self.button_up( button_type )
            time.sleep(options.click_down_delay)
    
## options of mouse related functions
options = ButtonOptions()

