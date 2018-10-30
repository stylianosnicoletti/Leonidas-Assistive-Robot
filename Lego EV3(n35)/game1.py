import ev3dev.ev3 as ev3
import sys
import helpers as hp
import json
import random
import paho.mqtt.client as mqtt
from time import sleep,time

client2 = mqtt.Client()
client2.connect("10.42.0.1",1883,60000)

def initializeSensors():
    lShoulder = ev3.LargeMotor('outA')
    rShoulder = ev3.LargeMotor('outB')
    lElbow = ev3.LargeMotor('outC')
    rElbow = ev3.LargeMotor('outD')
    rTouch = ev3.TouchSensor(ev3.INPUT_1)
    lTouch = ev3.TouchSensor(ev3.INPUT_2)
    return (lShoulder, rShoulder, lElbow, rElbow, rTouch, lTouch)

def move0():
    times = []
    lShoulder, rShoulder, lElbow, rElbow, rTouch, lTouch = initializeSensors()
    ev3.Sound.set_volume(100)
    ev3.Sound.speak("Let's play a game!")
    sleep(1.5)
    hp.setMotors([rShoulder, lShoulder],[450, -450])
    times.append(hp.waitForTouch([rTouch, lTouch], "both"))
    hp.setMotors([rShoulder, lShoulder], [0,0])
    ev3.Sound.speak('Well Done!')
    client2.publish("topic/rpi/dt",str(times))

def move13():
    lShoulder, rShoulder, lElbow, rElbow, rTouch, lTouch = initializeSensors()    
    hp.setMotors([rElbow],[350])
    hp.setMotors([rElbow],[-50])
    hp.setMotors([rElbow],[350])
    hp.setMotors([rElbow],[-50])
    hp.setMotors([rElbow],[350])
    hp.setMotors([rElbow],[0])
    client2.publish("topic/rpi/dt","Robot wiggled hand")    

# Say Hello and Wave Hands
def move1():
    
    lShoulder, rShoulder, lElbow, rElbow, rTouch, lTouch = initializeSensors()
    t = time()
    print(t)
    ev3.Sound.speak("Hello!")
    sleep(0.4)
    hp.setMotors([rElbow, lElbow],[350, 350])
    hp.setMotors([rElbow, lElbow],[-50, -50])
    hp.setMotors([rElbow, lElbow],[350, 350])
    hp.setMotors([rElbow, lElbow],[0, 0])
    client2.publish("topic/rpi/dt","Robot said Hello Message")
#    client2.disconect()

def move2():
    times=[]
    lShoulder, rShoulder, lElbow, rElbow, rTouch, lTouch = initializeSensors()
    t1 = time()
    for i in range(3):
        hp.setMotors([rShoulder, lShoulder], [-300, +300])
        hp.setMotors([rShoulder, lShoulder], [+550, -550])
        hp.setMotors([rShoulder, lShoulder], [0, 0])
        times.append(hp.waitForTouch([rTouch, lTouch]))
        hp.setMotors([rElbow, lElbow], [-150, -150])
        hp.setMotors([rElbow, lElbow], [0, 0])
        hp.setMotors([rElbow, lElbow], [150, 150])
        hp.setMotors([rShoulder, lShoulder, rElbow, lElbow] , [+550, -550, -150, -150])
        times.append(hp.waitForTouch([rTouch, lTouch],"both"))
        hp.setMotors([rElbow, lElbow], [150, 150])
        hp.setMotors([rShoulder, lShoulder], [0,0])
        hp.setMotors([rShoulder, lShoulder, rElbow, lElbow] , [-250, +250, +150, +150])
        hp.setMotors([rElbow, lElbow], [0, 0])
        hp.setMotors([rShoulder, lShoulder], [0,0])
    client2.publish("topic/rpi/dt",str(times))

def move3():
    times=[]
    for i in range(3):
        lShoulder, rShoulder, lElbow, rElbow, rTouch, lTouch = initializeSensors()
        hp.setMotors([rShoulder, rElbow], [-300, 150])
        times.append(hp.waitForTouch([rTouch],"right"))
        hp.setMotors([lShoulder, lElbow], [+300, 150])
        times.append(hp.waitForTouch([lTouch],"left"))
        hp.setMotors([rShoulder, rElbow], [0, 0])
        hp.setMotors([lShoulder, lElbow], [0, 0])
    client2.publish("topic/rpi/dt",str(times))
    
def move4():
    times=[]
    for i in range(3):
       lShoulder, rShoulder, lElbow, rElbow, rTouch, lTouch = initializeSensors()
       hp.setMotors([rShoulder, lShoulder],[-300, +300])
       times.append(hp.waitForTouch([rTouch,lTouch],"both"))
       hp.setMotors([rElbow, lElbow], [150, -150])
       hp.setMotors([rElbow, lElbow], [-150, 150])
       hp.setMotors([rElbow, lElbow], [0, 0])
       times.append(hp.waitForTouch([rTouch,lTouch],"both"))
       hp.setMotors([rShoulder, lShoulder],[300, -300])
       times.append(hp.waitForTouch([rTouch,lTouch],"both"))
       hp.setMotors([rElbow, lElbow], [150, -150])
       hp.setMotors([rElbow, lElbow], [-150, 150])
       hp.setMotors([rElbow, lElbow], [0, 0])
       times.append(hp.waitForTouch([rTouch,lTouch],"both"))
       hp.setMotors([rShoulder, lShoulder], [0,0])
    client2.publish("topic/rpi/dt",str(times))
    
def move5():
    times = []
    lShoulder, rShoulder, lElbow, rElbow, rTouch, lTouch = initializeSensors()
    for i in range(3):
        r = random.randint(2,5)
        if r == 2:
            hp.setMotors([rShoulder, lShoulder], [-300, +300])
            times.append(hp.waitForTouch([rTouch, lTouch], "both"))
            hp.setMotors([rElbow, lElbow], [150, -150])
            hp.setMotors([rElbow, lElbow], [-150, 150])
            hp.setMotors([rElbow, lElbow], [0, 0])
            times.append(hp.waitForTouch([rTouch,lTouch],"both"))
            hp.setMotors([rShoulder, lShoulder],[300, -300])
            times.append(hp.waitForTouch([rTouch,lTouch],"both"))
            hp.setMotors([rElbow, lElbow], [150, -150])
            hp.setMotors([rElbow, lElbow], [-150, 150])
            hp.setMotors([rElbow, lElbow], [0, 0])
            times.append(hp.waitForTouch([rTouch,lTouch],"both"))
            hp.setMotors([rShoulder, rShoulder], [0,0])
        elif r == 3:
            lShoulder, rShoulder, lElbow, rElbow, rTouch, lTouch = initializeSensors()
            hp.setMotors([rShoulder, rElbow], [-300, 150])
            times.append(hp.waitForTouch([rTouch],"right"))
            hp.setMotors([lShoulder, lElbow], [+300, 150])
            times.append(hp.waitForTouch([lTouch],"left"))
            hp.setMotors([rShoulder, rElbow], [0, 0])
            hp.setMotors([lShoulder, lElbow], [0, 0])
        elif r == 4:
            hp.setMotors([rShoulder, lShoulder], [-300, +300])
            hp.setMotors([rShoulder, lShoulder], [+300, -300])
            hp.setMotors([rShoulder, lShoulder], [0, 0])
            hp.setMotors([rElbow, lElbow], [-150, -150])
            hp.setMotors([rElbow, lElbow], [0, 0])
            hp.setMotors([rElbow, lElbow], [150, 150])
            hp.setMotors([rShoulder, lShoulder, rElbow, lElbow] , [+300, -300, -150, -150])
            times.append(hp.waitForTouch([rTouch, lTouch],"both"))
            hp.setMotors([rElbow, lElbow], [150, 150])
            hp.setMotors([rShoulder, lShoulder], [0,0])
            hp.setMotors([rShoulder, lShoulder, rElbow, lElbow] , [-250, +250, +150, +150])
            hp.setMotors([rElbow, lElbow], [0, 0])
            hp.setMotors([rShoulder, lShoulder], [0,0])
    client2.publish("topic/rpi/dt",str(times))
    
       
       

def memory(sequence):
    lenSeq = len(sequence)
    
    ev3.Sound.speak("Ready!")
    rTouch = ev3.TouchSensor(ev3.INPUT_1)
    lTouch = ev3.TouchSensor(ev3.INPUT_2)
    cTouch = ev3.TouchSensor(ev3.INPUT_3)
    score = 0 
    buttons = [rTouch, lTouch, cTouch]
    while (len(sequence) > 0):
        nextButton = int(sequence[0])
        for i,button in enumerate(buttons):
           doneAction = False 
           while buttons[i].value() > 0:
               if (not doneAction):
                   if ( i == nextButton ):
                       sequence = sequence[1:]
                       #print("Ah")
                       score+=1
                   else:
                       print("Mistakes have been done")
                       # Sends the score to rpi for the current game to rpi 
                       client2.publish("topic/rpi/dt",str("memory: " + str(score)))
                       ev3.Sound.speak("WRONG")
                       return False
               doneAction = True
    # Sends a successful completion of the current game to rpi
    ev3.Sound.speak("CORRECT")
    sleep(2.2)
    client2.publish("topic/rpi/dt",str("memory: " + "100")) 
    #ev3.Sound.speak("CORRECT")
    return True
	
def memoryWithTimer(sequence):
    lenSeq = len(sequence)
    ev3.Sound.speak("Ready!")
    rTouch = ev3.TouchSensor(ev3.INPUT_1)
    lTouch = ev3.TouchSensor(ev3.INPUT_2)
    cTouch = ev3.TouchSensor(ev3.INPUT_3)
    score = 0 
    buttons = [rTouch, lTouch, cTouch]
    # Set available time
    availableTime = hp.timeGiven(sequence)
    while (len(sequence) > 0):
        print("1)buttons values are " +"  available time " + str(availableTime) +" Still have time? " + str(hp.checkTimeAvailable(availableTime)))
        nextButton = int(sequence[0])
        for i,button in enumerate(buttons):
           doneAction = False 
           print("2)buttons values are " + str(buttons[i].value()) +"  available time " + str(availableTime) +" Still have time? " + str(hp.checkTimeAvailable(availableTime)))
           while (buttons[i].value() > 0):
               print("3)buttons values are " + str(buttons[i].value()) +"  available time " + str(availableTime) +" Still have time? " + str(hp.checkTimeAvailable(availableTime)))
               if (not doneAction):
                   if (i == nextButton):
                       sequence = sequence[1:]
                       #print("Ah")
                       score+=1
                   else:
                       print("Mistakes have been done")
                       # Sends the score to rpi for the current game to rpi 
                       client2.publish("topic/rpi/dt",str("memory: " + str(score)))
                       ev3.Sound.speak("WRONG")
                       return False
               doneAction = True
               if not hp.checkTimeAvailable(availableTime):       
                       print("Timeout")
                       # Sends the score to rpi for the current game to rpi 
                       client2.publish("topic/rpi/dt",str("memory: " + str(score)))
                       ev3.Sound.speak("Timeout")
                       return False
        if not hp.checkTimeAvailable(availableTime):
            print("TIMEOUT")
            # Sends the score to rpi for the current game to rpi 
            client2.publish("topic/rpi/dt",str("memory: " + str(score)))
            ev3.Sound.speak("TIMEOUT")
            return False

                
    print("4)buttons values are " + str(buttons[i].value()) +"  available time " + str(availableTime) +" Still have time? " + str(hp.checkTimeAvailable(availableTime)))
    # Sends a successful completion of the current game to rpi
    ev3.Sound.speak("CORRECT")
    sleep(2.2)
    client2.publish("topic/rpi/dt",str("memory: " + "100"))
    return True

#memoryWithTimer("10120")
