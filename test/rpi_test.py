"""EE 250L Lab 04 Starter Code

Run vm_publisher.py in a separate terminal on your VM."""
import paho.mqtt.client as mqtt
import time

#mqtt broker
broker = "amclq8tazzdq-ahrx7qvrwrf7.cedalo.dev"
myport = 1883

def on_connect(client, userdata, flags, rc):
    print("Connected to server (i.e., broker) with result code "+str(rc))

#Default message callback. Please use custom callbacks.
def on_message(client, userdata, msg):
    print("on_message: " + msg.topic + " " + str(msg.payload, "utf-8"))

if __name__ == '__main__':
    client = mqtt.Client()
    client.on_message = on_message
    client.on_connect = on_connect
    client.username_pw_set("Rpi", "password")
    client.connect(broker, port=myport, keepalive=60)
    client.publish("test1", "hello")
    client.loop_start()

    while True:
        time.sleep(1)
