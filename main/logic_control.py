from sr_emulator import *
from logger import log

def processEvents(events):
    log("Events: " + str(len(events)))
    for event in events:
        if type(event) == Marker:
            log("Marker: " + str(event))
        elif isinstance(tuple):
            log(str(event))
