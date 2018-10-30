from flask import Flask
from flask_ask import Ask, statement, convert_errors
import logging
from bluetooth import *
import paho.mqtt.client as mqtt
import RPi.GPIO as GPIO
import time
import paho.mqtt.client as mqtt
from os import system as sys
import subprocess
import random
import RPi.GPIO as GPIO
import time
import threading

clientEV3 = mqtt.Client()


app = Flask(__name__)
ask = Ask(app, '/')

pattern = ""
flag = True

logging.getLogger("flask_ask").setLevel(logging.DEBUG)
print ("running")

def lights(seq):
    GPIO.cleanup()
    GPIO.setmode(GPIO.BOARD)
    # pins for the + of the circuit
    pins = [36, 22, 32]
    # the closest grounds are [14,20,34]
    for digit in seq:
        num = pins[int(digit)]
        print(num)
        GPIO.cleanup()
        GPIO.setmode(GPIO.BOARD)
        GPIO.setup(num,GPIO.OUT)
        GPIO.output(num,1)
        time.sleep(1)
        GPIO.output(num,0)
        time.sleep(1)

def sequence_generator(size, game,chars="012"):
    global pattern
    if ((game % 3) == 0):
        pattern += str(''.join(random.choice(chars) for _ in range(size)))
    elif ((game % 3) == 1):
        pattern = str(''.join(random.choice(chars) for _ in range(size)))
    elif ((game % 3) == 2):
        pattern = str(''.join(random.choice(chars) for _ in range(size)))

def face_detection():
    print ("detecting user")
    subprocess.call("sudo -u pi python3 /home/pi/SDP-2018/Rpi/FaceDetection/faceDetection.py",shell=True)


@ask.intent('SetupLeo')
def setup():
    print ("Automatically Setup:")
    try:
        subprocess.call("sudo -u pi python /home/pi/SDP-2018/Rpi/Communication/initialisationScript.py",shell=True)
        return statement('Leo has set up')
    except:
        return statement('Fail to set up Leo, please try it again')

@ask.intent('ConnectLeo')
def connection():
    print("Connect Leo to Phone:")
    try:
        subprocess.call("sudo -u pi python3 /home/pi/SDP-2018/Rpi/Communication/mqttRpi.py",shell=True)
        return statement('Connecting to Leo')
    except:
        return statement('Fail to connect to Leo, please try it again')

@ask.intent('FaceMe')
def faceDetection():
    print("Make Leo Face to User:")
    try:
	t1 = threading.Thread(target = face_detection)
        t1.start()
        return statement('Leo is looking for you')
    except:
        return statement('Leo failed to find you, please try it again')


@ask.intent('PlayAtrick', mapping={'trick':'trick'})
def trick_game(trick):
    global flag
    if flag:
        clientEV3.connect("10.42.0.54", 1883, 60000)
        flag = False
    if trick == 'hello':
	clientEV3.publish("topic/ev3/dt", "351")
	return statement("Leo says hello")
    else:
	return statement("please say it again")

@ask.intent('memoryGame', mapping={'mode':'mode'})
def memory_game(mode):
    global pattern
    global flag
    print("playing memory game:", mode)
    if flag:
        clientEV3.connect("10.42.0.54", 1883, 60000)
        flag = False

    if mode == None:
	return statement("Please say it again")
    elif mode == "very easy":
        game = 2
        sequence_generator(size=5, game=game)
        lights(pattern)
        clientEV3.publish("topic/ev3/dt", str("356,"+pattern))

    elif mode == "easy":
        game = 0
        sequence_generator(size=2, game=game)
        lights(pattern)
        clientEV3.publish("topic/ev3/dt", str("356,"+pattern))

    elif mode == "normal":
        game = 5
        sequence_generator(size=5, game=game)
        lights(pattern)
        clientEV3.publish("topic/ev3/dt", str("357,"+pattern))

    elif mode == "hard":
        game = 1
        sequence_generator(size=2, game=game)
        lights(pattern)
        clientEV3.publish("topic/ev3/dt", str("356,"+pattern))

    elif mode == "very hard":
        game = 3
        sequence_generator(size=2, game=game)
        lights(pattern)
        clientEV3.publish("topic/ev3/dt", str("357,"+pattern))

    elif mode == "prestige":
        game = 4
        sequence_generator(size=2 ,game=game)
        lights(pattern)
        clientEV3.publish("topic/ev3/dt", str("357,"+pattern))

    else:
        return statement ('I do not know this game')
    return statement('Playing {} memory game'.format(mode))

@ask.intent('reactionGame', mapping={'game': 'game', 'num': 'num'})
def reaction_game(game, num):
    global flag
    if flag:
	clientEV3.connect("10.42.0.54", 1883, 60000)
	flag = False

    print ("playing game:", game, num)
    if game == 'reaction':
	print ("playing reaction game", int(num))
        if int(num) == 0:
            clientEV3.publish("topic/ev3/dt", "350")
	elif int(num) == 1:
	    clientEV3.publish("topic/ev3/dt", "352")
        elif int(num) == 2:
            clientEV3.publish("topic/ev3/dt", "353")
        elif int(num) == 3:
            clientEV3.publish("topic/ev3/dt", "354")
        elif int(num) == 4:
            clientEV3.publish("topic/ev3/dt", "355")
	else:
	    return statement ('I do not know this game')
    else:
	return statement ('I do not know this game')
    return statement('Playing {} game'.format(game))

if __name__ == '__main__':
    port = 5000
    app.run(host='127.0.0.1', port = port)
