#!/usr/bin/env python3

import paho.mqtt.client as mqtt

# This is the Publisher

client = mqtt.Client()
client.connect("10.42.0.180",1883,60)
client.publish("topic/motor-A/dt", "1");
client.publish("topic/motor-A/dt", "0");
client.disconnect();
