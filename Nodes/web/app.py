import paho.mqtt.client as mqtt
from flask import Flask, render_template, send_file, redirect
import sys
from cv2 import (VideoCapture, namedWindow, imshow, waitKey, destroyWindow, imwrite)
import cv2

#mqtt broker
broker = "amclq8tazzdq-ahrx7qvrwrf7.cedalo.dev"
myport = 1883
global status 
status = "Default"

def on_connect(client, userdata, flags, rc):
    print("Connected to server (i.e., broker) with result code "+str(rc))
    #subscribe to topics of interest here
    client.subscribe("alarm")
    
#Default message callback. Please use custom callbacks.
def on_message(client,userdata,msg):
    print("on_message: " + msg.topic + " " + str(msg.payload, "utf-8"))

#"S": stop current alarm
#"B": buglary  
#"F": fire
# Update Alarm Status
def alarm(client, userdata, msg):
	global status
	message = str(msg.payload, "utf-8")
	if message == "F":
		status = "Fire alert"
	elif message == "B":
		status = "Burglary alert"
	elif message == "S":
		status = "No Alert"	

app = Flask("Publishing")

# main page
@app.route('/')
def index():
	return render_template('index.html', alarm_status=status)

#
@app.route('/resetAlarm')
def resetAlarm():
	client.publish("alarm", "S")
	return render_template('sound.html')

@app.route('/soundAlarm')
def soundAlarm():
	client.publish("alarm", "B")
	return render_template('sound.html')


if __name__ == "__main__":
	client = mqtt.Client()
	client.on_message = on_message
	client.on_connect = on_connect
	client.username_pw_set("Cloud", "password")
	client.connect(broker, port=myport, keepalive=60)
	client.message_callback_add("alarm", alarm)
	client.loop_start()
	app.run(debug=False, host='0.0.0.0', port=5000)
	
