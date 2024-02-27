"""EE 250L Lab 04 Starter Code

Run vm_publisher.py in a separate terminal on your VM."""
import grovepi
# from grove_rgb_lcd import *
import paho.mqtt.client as mqtt
import time
import math

#mqtt broker
broker = "amclq8tazzdq-ahrx7qvrwrf7.cedalo.dev"
myport = 1883

#sensor ports
sonic = 2
dht = 3
buzzer = 4

grovepi.pinMode(buzzer,"OUTPUT")
def on_connect(client, userdata, flags, rc):
    print("Connected to server (i.e., broker) with result code "+str(rc))
    #subscribe to topics of interest here
    client.subscribe("alarm")

#Default message callback. Please use custom callbacks.
def on_message(client, userdata, msg):
    print("on_message: " + msg.topic + " " + str(msg.payload, "utf-8"))

def alarm(client, userdata, msg):
    alarm_type = str(msg.payload, "utf-8")
    global alarm_status
    if alarm_type == "F": #fire
        alarm_status = 1
    if alarm_type == "B": #burlary
        alarm_status = 1
    if alarm_type == "S": #stop existing alarm
        alarm_status = 0

if __name__ == '__main__':
    client = mqtt.Client()
    client.on_message = on_message
    client.on_connect = on_connect
    client.username_pw_set("Rpi", "password")
    client.connect(broker, port=myport, keepalive=60)
    client.message_callback_add("alarm", alarm)
    client.loop_start()
    global alarm_status
    alarm_status = 0
    while True:
        if alarm_status == 1:
            grovepi.digitalWrite(buzzer,1)
        else:
            grovepi.digitalWrite(buzzer,0)
        
        print(alarm_status)
        distance = grovepi.ultrasonicRead(sonic)
        sonic_msg = {
            "time":time.asctime(time.localtime()),
            "distance": distance,
        }
        client.publish("ultrasonic", str(sonic_msg))

        [temp,humi] = grovepi.dht(dht,0)  
        if math.isnan(temp) == False and math.isnan(humi) == False:
            dht_msg = {
                "time":time.asctime(time.localtime()),
                "temperature": temp,
                "humidity": humi,
            }
            client.publish("dht", str(dht_msg))

        time.sleep(2) #1
