# program to capture single image from webcam in python

# importing OpenCV library
import sys
from cv2 import (VideoCapture, namedWindow, imshow, waitKey, destroyWindow, imwrite)
import cv2

# initialize the camera
# If you have multiple camera connected with 
# current device, assign a value in cam_port
# variable according to that
cam_port = 0
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
    imwrite("/home/ancvirtual/ee250_finalProj_homeSecurity/face_recognizer/validation/unknown.png", image)
    quit()


    # If keyboard interrupt occurs, destroy image
    # window
    waitKey(0)
    destroyWindow("unknown")
    

# If captured image is corrupted, moving to else part
else:
    print("No image detected. Please! try again")
    

