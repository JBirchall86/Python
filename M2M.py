#!/usr/bin/env python

import serial
import paho.mqtt.client as mqtt

# Define event callbacks
def on_connect(mosq, obj, rc):
    print("rc: " + str(rc))

def on_message(mosq, obj, msg):
    print(msg.topic + " " + str(msg.qos) + " " + str(msg.payload))

def on_publish(mosq, obj, mid):
    print("mid: " + str(mid))

def on_subscribe(mosq, obj, mid, granted_qos):
    print("Subscribed: " + str(mid) + " " + str(granted_qos))

def on_log(mosq, obj, level, string):
    print(string)

mqttc = mqtt.Client()
# Assign event callbacks
mqttc.on_message = on_message
mqttc.on_connect = on_connect
mqttc.on_publish = on_publish
mqttc.on_subscribe = on_subscribe

# Create a serial object with Serial()
ser = serial.Serial(port = '/dev/ttyACM0', baudrate = 115200)
ser.timeout = 1
ser.bytesize = EIGHTBITS
ser.parity = PARITY_NONE
ser.xonxoff = FALSE
ser.rtscts = FALSE
ser.close()
ser.open()

# Flush buffers
ser.flushInput()
ser.flushOutput()

# Check modem is working
ser.write('AT\r\n')
data_raw = ser.readline()
if data_raw == 'OK\r\n':
    print("Connected To Modem")
else:
    print("Error Connecting To Modem")


# Set up loop here
    
# Modem wake here
ser.write('AT+CFUN=1\r\n')
# Delay to allow wake up
# Check for wake up, does modem reply OK on wake?
  
# Connect, note increased keep alive term
mqttc.connect("90.244.245.93",1883,120)

# Continue the network loop, exit when an error occurs

if  mqttc.loop(timeout = 1.0) == 0:
    # Perform keep alive connection


    # Prototype wireless sensor emulation loop
    # Publish a message
    mqttc.publish("myTopic", "my message")

#print("rc: " + str(rc))
    # Put modem to sleep
    ser.write('AT+CFUN=4\r\n')


