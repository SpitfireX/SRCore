from threading import Lock, current_thread
from time import strftime 

thread_lock = Lock()

def debug(message):
    thread_lock.acquire()
    
    timestamp = strftime("%H:%M:%S %d.%m.%Y ") 
    timestamp += current_thread().name
    timestamp += ":"
    
    print timestamp, message
    
    thread_lock.release()
