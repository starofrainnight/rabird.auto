'''
@date 2014-12-17
@author Hong-she Liang <starofrainnight@gmail.com>
'''

def switch_to_frame(self, frame):
    '''
    Added support switch to a frame where guide by the path.
    
    @param frame_path An array that contained frame ids how we could get to the
    final frame.
    '''
    if isinstance(frame, list):
        frame_path = frame
        for frame in frame_path:        
            self._old_switch_to_frame(frame)
    else:
        self._old_switch_to_frame(frame)
    
