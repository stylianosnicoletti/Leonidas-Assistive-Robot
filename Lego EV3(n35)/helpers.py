import ev3dev.ev3 as ev3
#import time
from time import sleep, time

"""
File containing helper functions used for robot movement
"""

FAST = 300
SLOW = 50

"""
Function used to wait for touch from the user
Currently waiting for infinity. Possible to update it with a timer
"""
def waitForTouch(sensors,string="both"):
    if string == "both":
        ev3.Sound.speak("Both")
    elif string == "left":
        ev3.Sound.speak("Left")
    elif string == "right":
        ev3.Sound.speak("Right")
    values = []
    for sensor in sensors:
        values.append(0)
    start = time()
    while True:
        positives = 0
        for i,sensor in enumerate(sensors):
            values[i] = values[i] + sensor.value()
            if values[i] > 0:
                positives += 1
        if positives == len(sensors):
            end = time()
            index = 0
            x = str(end-start)
            for i,c in enumerate(x):
               if c ==".":
                  index = i
            return (x[:index+3])

"""
Function that sets all the motors to the position they initially were in.
Input - a list of motors to be reset
Returns - nothing
"""
def resetMotors(motors, speed=SLOW):
    while True:
        if len(motors) == 0:
            break
        toRemove = []
        # Loop through the motors and adjust their position.
        for i,motor in enumerate(motors):
            if motor.position > 0:
                motor.run_forever(speed_sp = -speed)
                print( "Motor number " + str(i) + " at " + str(motor.position))
                if(motor.position <= 0):
                    motor.stop(stop_action="hold")
                    print("Remove motor " + str(i))
                    toRemove.append(motor)
                    continue
            elif motor.position < 0:
                print( "Motor number " + str(i) + " at " + str(motor.position))
                motor.run_forever(speed_sp = speed)
                if(motor.position >= 0):
                    motor.stop(stop_action="hold")
                    print(" Removing motor " + str(i))
                    toRemove.append(motor)
                    continue
            else:
                toRemove.append(motor)
                motor.stop(stop_action="hold")
                continue
        # Remove all the motors which are in the right position already.
        for mot in toRemove:
            motors.remove(mot)

"""
Function that sets motors into new positions.
Takes as input a list of motors and a list of positions
"""
def setMotors(motors, positions, speed=FAST):
    print(len(motors))
    print(len(positions))
    while True:
        if len(motors) == 0:
            break
        toRemove = []
        for i, motor in enumerate(motors):
            if motor.position > positions[i]:
                motor.run_forever(speed_sp = -speed)
                print( "Motor number " + str(i) + " at " + str(motor.position) + " MUST BE AT " + str(positions[i]))
                if(motor.position <= positions[i]):
                    motor.stop(stop_action="hold")
                    print("Remove motor " + str(i))
                    toRemove.append((motor, positions[i]))
                    continue
            elif motor.position < positions[i]:
                print( "Motor number " + str(i) + " at " + str(motor.position) + " MUST BE AT " + str(positions[i]))
                motor.run_forever(speed_sp = +speed)
                if(motor.position >= positions[i]):
                    motor.stop(stop_action="hold")
                    print(" Removing motor " + str(i))
                    toRemove.append((motor, positions[i]))
                    continue
            else:
                toRemove.append((motor, positions[i]))
                motor.stop(stop_action="hold")
                continue
        for (mot,pos) in toRemove:
            motors.remove(mot)
            positions.remove(pos)

def timeGiven(currentSequenceNum):
    print("Current Sequence Length" + str(len(currentSequenceNum)))
    # Returns the current time in seconds
    now = time()
    # Stopwatch time is equal to current time plus  (pattern size * 2 seconds) 
    future = now + (len(currentSequenceNum)*2)
    return future
	
def checkTimeAvailable(future):
    if (future > time()):
        return 1
    else:
        return 0
    print("No more available time")
	
	
