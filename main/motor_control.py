from sr_emulator import *
import time
import threading

thread = None
running = False

instructions = []

def initMotorControl(robot):
    print "Initializing MotorControl"
    r = robot
    thread = MotorCotrolThread(r)
    thread.start()
    
def addMotorInstruction(motors, speeds, duration = 0):
    i = MotorInstruction(motors, speeds, duration)
    instructions.append(i)
    
def skipCurrentInstruction():
    print thread
    thread.skip()

class MotorCotrolThread(threading.Thread):
    
    cI = None
    
    def __init__(self, robot):
        threading.Thread.__init__(self)
        self.r = robot

    def run(self):
        print "Started MotorControlThread"
        running = True
        
        while running:
            if len(instructions) > 0:
                cI = instructions.pop(0)
                cI.setup()
                cI.run()
            else:
                print "no instructions"
                cI = None
                for m in self.r.motors:
                    m.target = 0
        
    def skip(self):
        if self.cI != None:
            self.cI.skip()
                
class MotorInstruction():
    def __init__(self, motors, speeds, duration = 0):
        self.motors = motors
        self.speeds = speeds
        self.duration = duration
        self.skipped = False
        
    def setup(self):
        for i in range(len(self.motors)):
            self.motors[i].target = self.speeds[i]
    
    def run(self):
        print "running for", self.duration, "seconds"
        lasttime = time.time()
        
        if self.duration > 0:
            while not self.skipped:
                now = time.time()
                diff = now - lasttime
                self.duration -= diff
            
                if self.duration <= 0:
                    break
            
                lasttime = now
        else:
            while not self.skipped:
                time.sleep(0.01)
            
    def skip(self):
        self.skipped = True