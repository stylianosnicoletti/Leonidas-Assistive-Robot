#!/usr/bin/env python3
from bluetooth import *
import paho.mqtt.client as mqtt
import vlc
import time
import os

os.system("./chmodBluetooth.sh")

server_sock=BluetoothSocket( RFCOMM )
server_sock.bind(("",PORT_ANY))
server_sock.listen(1)

client = mqtt.Client()
client.connect("10.42.0.54", 1883, 60)

p = vlc.MediaPlayer("/home/pi/Desktop/zelda.mp3")

port = server_sock.getsockname()[1]

uuid = "94f39d29-7d6d-437d-973b-fba39e49d4ee"

advertise_service( server_sock, "SampleServer",
                   service_id = uuid,
                   service_classes = [ uuid, SERIAL_PORT_CLASS ],
                   profiles = [ SERIAL_PORT_PROFILE ], 
#                  protocols = [ OBEX_UUID ]
                    )

print("Waiting for connection on RFCOMM channel %d" % port)

def on_connect(client, userdata, flags, rc):
    print("Connected with result code "+str(rc))
    client.subscribe("topic/getMessage35/dt")
                     
def on_message(client, userdata, msg):
    data = msg.payload.decode()
    p.pause()
    client_sock.send(data + "!")
    print ("sending [%s]" % data)
    

client2 = mqtt.Client()
client2.connect("10.42.0.54",1883,60)
client2.on_connect = on_connect
client2.on_message = on_message

while True:
    print("Waiting for connection on RFCOMM channel %d" %port)
    client_sock, client_info = server_sock.accept()
    print("Accepted connection from ", client_info)

    try:
        data = client_sock.recv(1024).decode()
        if len(data) == 0:
            break
        print("received [%s]" % data)
        if data[:5] == 'game1':
            p.play()
            data = 'Playing game 1!'
            client.publish("topic/motor-A/dt", "0");
            
        elif data[:5] == 'game2':
            p.play()
            data = 'Playing game 2!'
            client.publish("topic/motor-A/dt", "1");
            
        elif data[:5] == 'game3':
            p.play()
            client.publish("topic/motor-A/dt", "2");
            data = 'Playing game 3!'
        else:
            data = 'Playing game 4!'
            os.system("python3 faceDetection.py")
        client2.loop_forever()
    
        
        

    except IOError:
        pass
    


print("disconnected")

client_sock.close()
server_sock.close()
print("all done")

