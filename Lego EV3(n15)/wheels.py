import ev3dev.ev3 as ev3
import sys 
import helpers as hp 
import paho.mqtt.client as mqtt
from time import sleep,time

client3 = mqtt.Client()
client3.connect("10.42.0.1",1883,60000)

def resetPositions():
    rWheel.position = 0
    lWheel.position = 0

def goBackwards(speed=500):
    rWheel, lWheel, gyroSensor = initializeSensors()
    rWheel.run_forever(speed_sp = -speed)
    lWheel.run_forever(speed_sp = speed)
   # ultraSonic = ev3.UltrasonicSensor(ev3.INPUT_2)
   # standard = ultraSonic.distance_centimeters
   # lookForEdge([rWheel,lWheel], ultraSonic, standard)

def goBackwardsForTime(speed=500,*,mTime):
    rWheel, lWheel, gyroSensor = initializeSensors()
    
    rWheel.run_forever(speed_sp = -speed)
    lWheel.run_forever(speed_sp = speed)
    sleep(mTime)
    rWheel.stop()
    lWheel.stop()
    client3.publish("topic/rpi/dt","Robot moved backward")

def goForwards(speed=500):
    rWheel, lWheel, gyroSensor = initializeSensors()
    rWheel.run_forever(speed_sp = speed)
    lWheel.run_forever(speed_sp = -speed)
   # ultraSonic = ev3.UltrasonicSensor(ev3.INPUT_3)
   # standard = ultraSonic.distance_centimeters
   # lookForEdge([rWheel,lWheel], ultraSonic, standard)

def goForwardsForTime(speed=500,*,mTime):
    rWheel, lWheel, gyroSensor = initializeSensors()
    rWheel.run_forever(speed_sp = speed)
    lWheel.run_forever(speed_sp = -speed)
    sleep(mTime)
    rWheel.stop()
    lWheel.stop()
   # ultraSonic = ev3.UltrasonicSensor(ev3.INPUT_2)
   # standard = ultraSonic.distance_centimeters
   # lookForEdge([rWheel,lWheel], ultraSonic, standard)
    client3.publish("topic/rpi/dt","Robot moved forward")


def stop():
    rWheel, lWheel, gyroSensor = initializeSensors()
    rWheel.stop(stop_action="hold")
    lWheel.stop(stop_action="hold")

def resetGyro():
    gyroSensor = ev3.GyroSensor(ev3.INPUT_1)
    gyroSensor.mode = 'GYRO-RATE'
    gyroSensor.mode = 'GYRO-ANG'

def initializeSensors():
    rWheel = ev3.MediumMotor('outA')
    lWheel = ev3.MediumMotor('outB')
    gyroSensor = ev3.GyroSensor(ev3.INPUT_1)
    return (rWheel, lWheel, gyroSensor)

def rotateClockwiseAtAngle(angle, speed=-500):
    rWheel, lWheel, gyroSensor = initializeSensors()
    resetGyro()
    while(gyroSensor.angle <= angle+1):
        #print(gyroSensor.angle)
        rWheel.run_forever(speed_sp = speed)
        lWheel.run_forever(speed_sp = speed)
    rWheel.stop(stop_action="hold")
    lWheel.stop(stop_action="hold")
    if(angle == 90):
        client3.publish("topic/rpi/dt","Robot turned around")
    elif(angle ==360):
        client3.publish("topic/rpi/dt","Robot made a spin")


def rotateAntiClockwiseAtAngle(angle, speed=-500):
    rWheel, lWheel, gyroSensor = initializeSensors()
    resetGyro()
    angle = - abs(angle)
    while(gyroSensor.angle >= angle-1):
        print(gyroSensor.angle)
        rWheel.run_forever(speed_sp = speed)
        lWheel.run_forever(speed_sp = speed)
    rWheel.stop(stop_action="hold")
    lWheel.stop(stop_action="hold")

def rotateClockwise(speed=-300):
    rWheel, lWheel, gyroSensor = initializeSensors()
    resetGyro()
    rWheel.run_forever(speed_sp = speed)
    lWheel.run_forever(speed_sp = speed)

def rotateAntiClockwise(speed=300):
    rWheel, lWheel, gyroSensor = initializeSensors()
    resetGyro()
    rWheel.run_forever(speed_sp = speed)
    lWheel.run_forever(speed_sp = speed)

def lookForEdge(standard=4.0):
    ultraSonic1 = ev3.UltrasonicSensor(ev3.INPUT_2)
    ultraSonic2 = ev3.UltrasonicSensor(ev3.INPUT_3)
    while True:
        #print(ultraSonic1.distance_centimeters)
        #print(ultraSonic2.distance_centimeters)   
        if ultraSonic1.distance_centimeters > 2*standard or ultraSonic2.distance_centimeters > 2 * standard:
            stop()

#goBackwardsForTime(mTime=1.5)
#goForwardsForTime(mTime=1.5)
#rotateClockwiseAtAngle(angle = 360)
#rotateClockwiseAtAngle(angle = 180)
