
import re
# Import the global logging unit, not our logging .
psutil = __import__('psutil')

def killall(name_pattern):
    """
    A simple method to killall process just matched the name pattern .
    
    @arg name_pattern In python re module's pattern format
    """   
    process_list = []
    for proc in psutil.process_iter():
        if re.match(name_pattern, proc.name()):
            process_list.append(proc)
        
    for p in process_list:
        try:
            p.terminate()
        except:
            pass
         
    gone, alive = psutil.wait_procs(process_list, timeout=3)
    for p in alive:
        try:
            p.kill()
        except:
            pass
