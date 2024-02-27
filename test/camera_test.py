"""EE 250L Lab 04 Starter Code

Run vm_publisher.py in a separate terminal on your VM."""
import paho.mqtt.client as mqtt
import time
import sys
from cv2 import (VideoCapture, namedWindow, imshow, waitKey, destroyWindow, imwrite)
import cv2
import os

#mqtt broker
broker = "amclq8tazzdq-ahrx7qvrwrf7.cedalo.dev"
myport = 1883

def on_connect(client, userdata, flags, rc):
    print("Connected to server (i.e., broker) with result code "+str(rc))
    #subscribe to topics of interest here
    client.subscribe("test2")

#Default message callback. Please use custom callbacks.
def on_message(client, userdata, msg):
    print("on_message: " + msg.topic + " " + str(msg.payload, "utf-8"))

def camera(client, userdata, msg):
     # initialize the camera
     # If you have multiple camera connected with 
     # current device, assign a value in cam_port
     # variable according to that
     cam_port = 0
     cam = cv2.VideoCapture(cam_port)
     # reading the input using the camera
     result, image = cam.read()
     cam.release()
     cv2.imwrite("send.png", image)
     with open("send.png",'rb') as file:
         img = file.read()
         img_byte = bytearray(img)
     # os.remove("send.png")
     client.publish("test3", img_byte,2)
     print("image published")


if __name__ == '__main__':
    client = mqtt.Client()
    client.on_message = on_message
    client.on_connect = on_connect
    client.username_pw_set("Camera", "password")
    client.connect(broker, port=myport, keepalive=60)
    client.message_callback_add("test2", camera)
    client.loop_start()

    while True:
        time.sleep(1)
