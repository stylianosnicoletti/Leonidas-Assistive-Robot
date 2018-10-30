#!/usr/bin/env python3

from bluetooth import *
import paho.mqtt.client as mqtt
#import vlc
import os
import string
import random
import RPi.GPIO as GPIO
import time

#os.system("./")
def lights(seq):
    GPIO.cleanup()
    GPIO.setmode(GPIO.BOARD)
    # pins for the + of the circuit
    pins = [36, 16, 32]
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

#lights("021021")
playingGame = False
pattern =""
score =0
game = 0
clientPhone = mqtt.Client()
clientPhone.connect("10.42.0.1", 1883, 60000)
clientEV3 = mqtt.Client()
clientEV3.connect("10.42.0.54", 1883, 60000)
#clientEV3bottom = mqtt.Client()
#clientEV3bottom.connect("10.42.0.180", 1883, 60000)

#p = vlc.MediaPlayer("/home/pi/Desktop/zelda.mp3")

# Formula to return the divisor : (n^2 * n) / 2
def formula(outOf):
    return int((((outOf*outOf)+outOf)/2)-1)

# Return a random sequence
def sequence_generator(chars="012",*,size, game):
    global pattern
    if ((game % 3) == 0):
        pattern += str(''.join(random.choice(chars) for _ in range(size)))
    elif ((game % 3) == 1):
        pattern = str(''.join(random.choice(chars) for _ in range(size)))
    elif ((game % 3) == 2):
        pattern = str(''.join(random.choice(chars) for _ in range(size)))

def on_connect(client, userdata, flags, rc):
    print("Connected with result code " +str(rc))
    client.subscribe("topic/rpi/dt")

def on_message(client, userdata, msg):
    global pattern
    global score
    global game
    global playingGame
    data = str(msg.payload)
    print(data)
    ######### Phone -> Rpi -> EV3 #########
    
    # Demo Reaction Game
    if(data == "b'0'" and not playingGame):
        clientEV3.publish("topic/ev3/dt", "350")
        playingGame = True
        #p.play()
    # Hello
    elif(data == "b'1'" and not playingGame):
       #Remove the sleep
       #time.sleep(3)
        clientEV3.publish("topic/ev3/dt", "351")
        playingGame = True
        #p.play()
    # Reaction Game 1
    elif(data == "b'2'" and not playingGame):
        clientEV3.publish("topic/ev3/dt", "352")
        playingGame = True
        #p.play()
    # Reaction Game 2
    elif(data == "b'3'" and not playingGame):
        clientEV3.publish("topic/ev3/dt", "353")
        playingGame = True
        #p.play()
    # Reaction Game 3
    elif(data == "b'4'" and not playingGame):
        clientEV3.publish("topic/ev3/dt", "354")
        playingGame = True
        #p.play()
    # Reaction Game 4
    elif(data == "b'5'" and not playingGame):
        #time.sleep(4)
        clientEV3.publish("topic/ev3/dt", "355")
        playingGame = True
        #p.play()
    elif(data == "b'6'" and not playingGame):
        playingGame = True;
        os.system("python3 /home/pi/SDP-2018/Rpi/FaceDetection/faceDetection.py")
    elif(data == "b'7'" and not playingGame):
        # Memory game PRESTIGE
        game = 4
        score = 0
        sequence_generator(size=2 ,game=game)
        lights(pattern)
        clientEV3.publish("topic/ev3/dt", str("357,"+pattern))
        playingGame = True
    elif(data == "b'8'" and not playingGame):
        # Memory game VERY EASY
        game = 2
        score = 0
        sequence_generator(size=5, game=game)
        lights(pattern)
        clientEV3.publish("topic/ev3/dt", str("356,"+pattern))
        playingGame = True
    elif(data == "b'9'" and not playingGame):
        #p.play()
        # Memory game EASY
        game = 0
        score = 0
        sequence_generator(size=2, game=game)
        lights(pattern)
        clientEV3.publish("topic/ev3/dt", str("356,"+pattern))
        #p.play()
        playingGame = True
    elif(data == "b'10'" and not playingGame):
        # Memory game NORMAL
        #time.sleep(4)
        game = 5
        score = 0
        sequence_generator(size=5, game=game)
        lights(pattern)
        clientEV3.publish("topic/ev3/dt", str("357,"+pattern))
        playingGame = True
    elif(data == "b'11'" and not playingGame):
        # Memory game HARD
        game = 1
        score = 0
        sequence_generator(size=2, game=game)
        lights(pattern)
        clientEV3.publish("topic/ev3/dt", str("356,"+pattern))
        playingGame = True
    elif(data == "b'12'" and not playingGame):
        # Memory game VERY HARD
        game = 3
        score = 0
        sequence_generator(size=2, game=game)
        lights(pattern)
        clientEV3.publish("topic/ev3/dt", str("357,"+pattern))
        playingGame = True

    elif(data == "b'13'" and not playingGame):
        # Wiggle Hand
        clientEV3.publish("topic/ev3/dt", str("513"))
        playingGame = True

    elif(data == "b'14'" and not playingGame):
        # Go Forward
        #time.sleep(3)
        #clientEV3bottom.publish("topic/motor-A/dt", str("1514"))
        playingGame = True
   
    elif(data == "b'15'" and not playingGame):
        # Go Backwards
        # clientEV3bottom.publish("topic/motor-A/dt", str("1515"))
        playingGame = True
    
    elif(data == "b'16'" and not playingGame):
        # Turn Around
        #clientEV3bottom.publish("topic/motor-A/dt", str("1516"))
        playingGame = True
   
    elif(data == "b'17'" and not playingGame):
        # Spin
        # remove sleep
        #time.sleep(3)
        #clientEV3bottom.publish("topic/motor-A/dt", str("1517"))
        playingGame = True




    elif(data == "b'-1'"):
        clientEV3.disconnect()
    ####### Memory part #######

    # If the user completes current stage
    elif(data == "b'memory: 100'"):

        # Update score
        score+=len(pattern)

        # Stop when the size of the pattern is larger than 10, which is dettermined the last stage
        if(len(pattern) >=10 and game % 3 <= 1):
            # p.pause()
            # Sending results to app after successful completion of game eg. Score 55/55
            clientPhone.publish("topic/android/dt", "Score: "+str(score)+ "/" + str(formula(len(pattern))))
            # Resetting pattern and score
            pattern=""
            score = 0
            game = -1
            playingGame = False
        elif((game%3) == 0):
            # Add one random touch to the pattern
            sequence_generator(size=1, game=game)
            print("Light")
            lights(pattern)
            # Run the new pattern on EV3 (with or without timer)
            if game == 0:
                print("sending")
                clientEV3.publish("topic/ev3/dt", str("356,"+pattern))
            elif game == 3:
                clientEV3.publish("topic/ev3/dt", str("357,"+pattern))
        elif((game%3) == 1):
            # Create a new entire sequence
            x = len(pattern) + 1
            sequence_generator(size=x, game=game)
            lights(pattern)

            # Run the new pattern on EV3 (with or without timer)
            if game == 1:
                clientEV3.publish("topic/ev3/dt", str("356,"+pattern))
            elif game == 4:
                clientEV3.publish("topic/ev3/dt", str("357,"+pattern))
        elif(((game % 3) == 2) and (score >= 50)):
            # Game was won
            # Sending results to app after successful completion of game eg. Score 55/55
            clientPhone.publish("topic/android/dt", "b'Score: "+str(score)+ "/" + str(formula(len(pattern))))
            # Resetting pattern and score
            pattern=""
            score = 0
            game = -1
            playingGame = False
        elif((game % 3) == 2):
            sequence_generator(size=5, game=game)
            lights(pattern)

            if game == 2:
                clientEV3.publish("topic/ev3/dt", str("356,"+pattern))
            elif game == 5:
                clientEV3.publish("topic/ev3/dt", str("357,"+pattern))
    # If the user fails to complete the current stag
    elif(data[:9] == "b'memory:"):
        #p.pause()
        print("whatever")
        #Update score
        score+=int(data[10:len(data)-1])
        print (score)

        # Sending results to app after a wrong touch eg. Score 6/9
        clientPhone.publish("topic/android/dt", "b'Score: "+str(score))
        print
        print( "msg send")
        # Resetting pattern and score
        pattern=""
        score = 0
        game = -1
        playingGame = False


    ###### EV3 -> Rpi -> Phone ######
    elif('.' in data or 'H' in data or 'R' in data):
        print("Received")
        print(data)
        playingGame = False
        clientPhone.publish("topic/android/dt", data)
        #p.pause()
    #else:
       # playingGame = False


clientPhone.on_connect = on_connect
clientPhone.on_message = on_message
clientPhone.loop_forever()
