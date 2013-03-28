from sr_emulator import *
from logger import debug

def processEvents(events):
    # log("Events: " + str(len(events)))
    for event in events:
        if event.eventType == "Marker":
            debug("Marker: " + str(event))
        # elif event.eventType == "Pin":
        #     log("Pin: "str(event))
