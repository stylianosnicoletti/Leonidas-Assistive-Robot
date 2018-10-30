#!/usr/bin/env python3
import paho.mqtt.client as mqtt
import helpers as hp
import wheels
from threading import Thread
from ev3dev.auto import *


#This is the Subscriber
def representsInt(s):
    try:
        int(s)
        return True
    except ValueError:
        return False

def on_connect(client, userdata, flags, rc):
    print("Connected with result code "+str(rc))
    client.subscribe("topic/motor-A/dt")
    try:
        t = Thread(target =  wheels.lookForEdge)
        t.start()  
    except:
        print("Unable to start thread")

def on_message(client, userdata, msg):
    if (msg.payload.isalpha()):
        client.disconnect()
    elif (int(msg.payload) == 0):
        print ("foward")
        wheels.goForwards()
    elif (int(msg.payload) == 1):
        print ("backword")
        wheels.goBackwards()
    elif (int(msg.payload) == 2):
        print("clockwise")
        wheels.rotateClockwise()
    elif (int(msg.payload) == 3):
        print("anticlockwise")
        wheels.rotateAntiClockwise()
    elif (int(msg.payload) == 4):
        wheels.stop()
    elif (int(msg.payload) == 1514):
        print("1514 Forward")
        wheels.goForwardsForTime(mTime=3.5)
    elif (int(msg.payload) == 1515):
        print("1515 Backward")
        wheels.goBackwardsForTime(mTime=3.5)
    elif (int(msg.payload) == 1516):
        print("1516 Turn around")
        wheels.rotateClockwiseAtAngle(angle = 90)
    elif (int(msg.payload) == 1517):
        print("1517 Spin")
        wheels.rotateClockwiseAtAngle(angle = 360)


def subscriber():
    client = mqtt.Client()
    client.connect("10.42.0.180",1883,60)

    client.on_connect = on_connect
    client.on_message = on_message

	#m.run_direct()
	#m.duty_cycle_sp=0

    client.loop_forever()

while True:
    try:
        subscriber()
    except:
        pass
