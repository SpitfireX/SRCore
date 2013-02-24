from sr_emulator import *
from logger import log

def processEvents(events):
    # log("Events: " + str(len(events)))
    for event in events:
        if event.eventType == "Marker":
            log("Marker: " + str(event))
        elif event.eventType == "Pin":
            log(str(event))
