# ee250_finalProj_homeSecurity

#### Team Members: Renzhi Li and Anchal Srivastava

## Code Compiling/Execution
- Use 4 terminals
	- Local VM runs camera.py
	- SSH into Azure VM
		- This runs cloud.py
	- SSH into RaspberryPi
		- This shoudl run rpi.py
	- The webfront is run with app.py which we ran on a local VM terminal window (same VM that runs the camera.py)
- RPI is connected to GrovePi sensors
	- Digital Temp/Humidity Sensor connected to port D3
	- Ultrasonic Ranger connected to port D2
	- Buzzer connected to port D4
- Make sure webcam is enabled on local VM

## External Libraries Used
- Face Recognition
	- face_recognition (Python)
	- numpy (Python)
	- pickle (Python)
	- Pillow (not used in final code; only used during testing)
- Communication
	- Eclipse Paho MQTT Python
- Camera
	- OpenCV (Python)

## To Do List
1. Encrytpion
- [ ] Rpi private & public key
- [ ] Computer private & public key
- [ ] Server pirvate & public key

2. Sensors and Rpi
- [ ] Connect Sensor to Rpi and Read data
- [ ] Suscribe to MQTT topics "/alarm"
- [ ] To send data to the Server, Encrypt with Server's public key and then the Rpi's private key
- [ ] To decrypt data from Server, Decrypt with Server's public key and then Rpi's public key

3. Computer Camera
- [ ] Suscribe to MQTT "/cameraTrigger"
- [ ] if camera is triggered, take an image and publish it to "/camera" with encryption

4. Cloud Server
- [ ] Setup MQTT Broker - RL
- [ ] Decrypt and store data from rpi (for up till 7 days?)
- [ ] If ultrasonic sensor within alarm range, publish trigger message encrypted with Computer's public key and then Server's private key, under "/cameraTrigger"
- [ ] process the image 
   
