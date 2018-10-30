#!/usr/bin/env python3
import paho.mqtt.client as mqtt
import game1
import helpers as hp
from time import time
from ev3dev.auto import *

# This is the Subscriber
global flag
flag = True

def on_connect(client, userdata, flags, rc):
    print("Connected with result code "+str(rc))
    client.subscribe("topic/ev3/dt")

def on_message(client, userdata, msg):
    data = str(msg.payload)
    global flag
    if flag:
        flag = False
        send_message(data)
        flag = True

def send_message(data):
    if (len(data)>6):
        #play memory game
        #expecting a message of form "b'356,XXXXX'"
        #XXXX denotes the sequence of buttons, X is 0, 1 or 2
        (code, sequence) = data.split(",") # Split data on comma
        sequence = sequence[:-1] # Just to remove the ' at the end of the sequence
        print(sequence)
        if(code == "b'356"):
            game1.memory(sequence)
        elif(code == "b'357"):
            game1.memoryWithTimer(sequence)
    elif(data == "b'350'"):
        game1.move0()

    elif(data == "b'351'"):
        game1.move1()

    elif(data == "b'352'"):
        game1.move2()
    
    elif(data == "b'353'"):
        game1.move3()
    
    elif(data == "b'354'"):
        game1.move4()
    
    elif(data == "b'355'"):
        game1.move5()
    elif(data == "b'513'"):
        game1.move13()

client = mqtt.Client()
client.connect("10.42.0.54",1883,60000)
client.on_connect = on_connect
client.on_message = on_message
client.loop_forever()
