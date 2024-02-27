from flask import Flask, render_template, send_file
import sys
from cv2 import (VideoCapture, namedWindow, imshow, waitKey, destroyWindow, imwrite)
import cv2

app = Flask("Publishing")

@app.route('/')
def index():
	return render_template('index.html')
 
@app.route('/get_saved_image')
def get_saved_image():
	image_path = 'face_recognizer/validation/unknown.png'
	return send_file(image_path, mimetype='image/png', as_attachment=True)
	
@app.route('/captureImage')
def captureImage():
	cam_port = -1
	cam = cv2.VideoCapture(cam_port)

	# reading the input using the camera
	result, image = cam.read()
	cam.release()

	# If image will detected without any error,
	# show result
	if result:

	    # showing result, it take frame name and image
	    # output
	    imshow("unknown", image)

	    # saving image in local storage
	    imwrite("face_recognizer/validation/unknown.png", image)
	  


	    # If keyboard interrupt occurs, destroy image
	    # window
	    waitKey(0)
	    destroyWindow("unknown")
	quit()
	
	


if __name__ == "__main__":
	app.run(debug=False, host='0.0.0.0', port=5000)
	
