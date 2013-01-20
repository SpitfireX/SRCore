from threading import Lock, current_thread
from time import strftime 

thread_lock = Lock()

def log(message):
    thread_lock.acquire()
    
    timestamp = strftime("%H:%M:%S %d.%m.%Y ") 
    timestamp += current_thread().name
    timestamp += ":"
    
    print timestamp, message
    
    logfile=open("log.txt", "a"); # Nur rin Vorschlag, um den Log auch in einer Datei auf dem USB-Stick
    logfile.write(timestamp+" "+message) #zu haben. Könnte nützlich sein, um später Fehler zu checken o.ä.
    logfile.close() #ihr könnt das aber auch auskommentieren, wenn ihr wollt. -Max
    
    thread_lock.release()
