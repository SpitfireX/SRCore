from sr_emulator import *
import time
import threading

thread = None
r = None

class MotorCotrolThread(threading.Thread):
    instructions = []
    
    def __init__(self):
        threading.Thread.__init__(self)

    def run(self):
        print "Started MotorControlThread"
        
        while True:
            i = instructions[0]
            
            if len(instructions) == 0:
                print "no instructions"
                for m in r.motors:
                        m.target = 0
            else:
                index = 0
                
                for m in i.motors:
                    print "instruction:", i.motors, i.speeds, i.duration
                    m.target = i.speeds[index]
                    index += 1
                    
                time.sleep(i.duration)
                instructions = instructions[1:len(instructions)]

class MotorInstruction():
    motors = []
    speeds = []
    duration = None
    
    def _init_(self, motors, speeds, duration = 0):
        self.motors = motors
        self.speeds = speeds
        self.duration = duration

def initMotorControl(robot):
    print "Initializing MotorControl"
    r = robot
    thread = MotorCotrolThread()
    thread.start()
    
def addMotorInstruction(motors, speeds, duration = 0):
    i = MotorInstruction(motors, speeds, duration)
    instructions.append(i)