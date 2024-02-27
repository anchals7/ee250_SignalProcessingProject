"""EE 250L Lab 04 Starter Code

Run vm_publisher.py in a separate terminal on your VM."""
import paho.mqtt.client as mqtt
import time
from cv2 import (VideoCapture, namedWindow, imshow, waitKey, destroyWindow, imwrite)
import cv2

#mqtt broker
broker = "amclq8tazzdq-ahrx7qvrwrf7.cedalo.dev"
myport = 1883

def on_connect(client, userdata, flags, rc):
    print("Connected to server (i.e., broker) with result code "+str(rc))
    #subscribe to topics of interest here
    client.subscribe("cameraTrigger")

#Default message callback. Please use custom callbacks.
def on_message(client, userdata, msg):
    print("on_message: " + msg.topic + " " + str(msg.payload, "utf-8"))

def camera(client, userdata, msg):
	 # initialize the camera
     # If multiple cameras are connected to current device, 
     # assign a value in cam_port accordingly
     cam_port = 0
     cam = cv2.VideoCapture(cam_port)
     # reading the input with camera
     result, image = cam.read()
     cam.release()
     cv2.imwrite("send.png", image) # save the capture in current folder
     # read captured image file as bytearray
     with open("send.png",'rb') as file:
         img = file.read()
         img_byte = bytearray(img)
     os.remove("send.png") # remove captured image locally
     client.publish("camera", img_byte)# send the captured image through mqtt

if __name__ == '__main__':
    client = mqtt.Client()
    client.on_message = on_message
    client.on_connect = on_connect
    client.username_pw_set("Camera", "password")
    client.connect(broker, port=myport, keepalive=60)
    client.message_callback_add("cameraTrigger", camera)
    client.loop_start()

    while True:
        time.sleep(1)
