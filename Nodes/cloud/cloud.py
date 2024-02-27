"""EE 250L Lab 04 Starter Code

Run vm_publisher.py in a separate terminal on your VM."""
import paho.mqtt.client as mqtt
import time
import json

import pickle
from collections import Counter
from pathlib import Path

import face_recognition
from PIL import Image, ImageDraw

DEFAULT_ENCODINGS_PATH = Path("output/encodings.pkl")
BOUNDING_BOX_COLOR = "blue"
TEXT_COLOR = "white"

#mqtt broker
broker = "amclq8tazzdq-ahrx7qvrwrf7.cedalo.dev"
myport = 1883

def on_connect(client, userdata, flags, rc):
    print("Connected to server (i.e., broker) with result code "+str(rc))
    #subscribe to topics of interest
    client.subscribe("ultrasonic")
    client.subscribe("dht")
    client.subscribe("camera")

#Default message callback. Please use custom callbacks.
def on_message(client,userdata,msg):
    print("on_message: " + msg.topic + " " + str(msg.payload, "utf-8"))

def ultrasonic(client,userdata,msg):
    # convert received bytearray to json
    message = json.loads(msg.payload.decode('utf8').replace("'", '"'))
    time = message["time"]
    distance = message["distance"]
    # store sensor data in cloud
    with open('ultrasonic.txt', 'a') as file:
        file.write(str(time)+ " " + str(distance) +'\n')
    # if object is detected within 100 cm of the ultrasonic sensor, sound alarm
    if distance <= 100:
        print("Camera Triggered")
        client.publish("cameraTrigger", "C")

def dht(client, userdata, msg):
    # convert received bytearray to json
    message = json.loads(msg.payload.decode('utf8').replace("'", '"'))
    print(message)
    time = message["time"]
    temperature = message["temperature"]
    humidity = message["humidity"]
    # store sensor data in cloud
    with open('dht.txt', 'a') as file:
        file.write(str(time) + " " + str(temperature) + " " + str(humidity) +'\n')
    
    if temperature > 40:
        client.publish("alarm","F")

# image processing here
def recognition(client, userdata,msg):
    image = msg.payload
    with open("receive.png", 'wb') as file:
        file.write(image)  
    # Create directories if they don't already exist
    
    Path("training").mkdir(exist_ok=True)
    Path("output").mkdir(exist_ok=True)
    Path("validation").mkdir(exist_ok=True)
    print("image received")
    encode_known_faces()
    alert_name = recognize_faces("receive.png")
    print("image validated")
    if alert_name == "Unknown":
    	client.publish("alarm", "B")
    	

def encode_known_faces(
    model: str = "hog", encodings_location: Path = DEFAULT_ENCODINGS_PATH
) -> None:
    """
    Loads images in the training directory and builds a dictionary of their
    names and encodings.
    """
    names = []
    encodings = []
    for filepath in Path("training").glob("*/*"):
        name = filepath.parent.name
        image = face_recognition.load_image_file(filepath)

        face_locations = face_recognition.face_locations(image, model=model)
        face_encodings = face_recognition.face_encodings(image, face_locations)

        for encoding in face_encodings:
            names.append(name)
            encodings.append(encoding)

    name_encodings = {"names": names, "encodings": encodings}
    with encodings_location.open(mode="wb") as f:
        pickle.dump(name_encodings, f)
        
def recognize_faces(
    image_location: str,
    model: str = "hog",
    encodings_location: Path = DEFAULT_ENCODINGS_PATH,
) -> None:
    """
    Given an unknown image, get the locations and encodings of any faces and
    compares them against the known encodings to find potential matches.
    """
    with encodings_location.open(mode="rb") as f:
        loaded_encodings = pickle.load(f)

    input_image = face_recognition.load_image_file(image_location)

    input_face_locations = face_recognition.face_locations(
        input_image, model=model
    )
    input_face_encodings = face_recognition.face_encodings(
        input_image, input_face_locations
    )


    for unknown_encoding in zip(
        input_face_locations, input_face_encodings
    ):
        name = _recognize_face(unknown_encoding, loaded_encodings)
        if not name:
            # name = "Unknown"
            print("Unknown")
            return "Unknown"
        else:
            print(name)
            return name
    
    
def _recognize_face(unknown_encoding, loaded_encodings):
    """
    Given an unknown encoding and all known encodings, find the known
    encoding with the most matches.
    """
    boolean_matches = face_recognition.compare_faces(
        loaded_encodings["encodings"], unknown_encoding
    )
    votes = Counter(
        name
        for match, name in zip(boolean_matches, loaded_encodings["names"])
        if match
    )
    if votes:
        return votes.most_common(1)[0][0]
        
    
    
def validate(model: str = "hog"):
    """
    Runs recognize_faces on a set of images with known faces to validate
    known encodings.
    """
    for filepath in Path("validation").rglob("*"):
        if filepath.is_file():
            recognize_faces(
                image_location=str(filepath.absolute()), model=model
            )
         


if __name__ == '__main__':
    client = mqtt.Client()
    client.on_message = on_message
    client.on_connect = on_connect
    client.username_pw_set("Cloud", "password")
    client.connect(broker, port=myport, keepalive=60)
    client.message_callback_add("ultrasonic", ultrasonic)
    client.message_callback_add("dht", dht)
    # client.message_callback_add("camera", recognition)
    client.loop_start()

    while True:
        time.sleep(1)
