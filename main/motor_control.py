from sr_emulator import *
from logger import log
import time
import threading

instructions = []

class MotorCotrolThread(threading.Thread):  
    cI = None
    
    def __init__(self):
        threading.Thread.__init__(self)
        self.name = "MotorControl"

    def run(self):
        log("Started MotorControl Thread")
        
        global running
        running = True
        
        while running:
            global cI
            if len(instructions) > 0:
                cI = instructions.pop(0)
                cI.setup()
                cI.run()
            else:
                #log("no instructions")
                cI = None
                for m in r.motors:
                    m.target = 0
        
    def skip(self):
        if cI is not None:
            cI.skipped = True
            log("    skipping instruction")
        else:
            log("    noting to skip")
                
class MotorInstruction():
    def __init__(self, motors, speeds, duration = 0):
        self.motors = motors
        self.speeds = speeds
        self.duration = duration
        self.skipped = False
        
    def setup(self):
        #log("Instruction: " + str(self.motors) + " " + str(self.speeds) + " " + str(self.duration))
        for i in range(len(self.motors)):
            self.motors[i].target = self.speeds[i]
    
    def run(self):
        lasttime = time.time()
        
        if self.duration > 0:
            log("running for " + str(self.duration) + " seconds")
            while not self.skipped:
                now = time.time()
                diff = now - lasttime
                self.duration -= diff
            
                if self.duration <= 0:
                    break
            
                lasttime = now
        else:
            log("running for indefinite time")
            while not self.skipped:
                time.sleep(0.1)
        
def initMotorControl(robot):
    log("Initializing MotorControl")
    
    global r
    r = robot
    
    global thread
    thread = MotorCotrolThread()
    
    global running
    running = False
    
def startThread():
    thread.start()

def stopThread():
    global running
    running = False
    
def addMotorInstruction(motors, speeds, duration = 0):
    i = MotorInstruction(motors, speeds, duration)
    instructions.append(i)
    
def skipCurrentInstruction():
    log ("Attempting to skip instruction")
    thread.skip()