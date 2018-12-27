#!/usr/bin/env python
from imutils import paths
import argparse
import cv2
import os

# calculates variance of laplacian 
def var_lap(image):
	return cv2.Laplacian(image, cv2.CV_64F).var()

# instantiate capture device--make sure to change value if multiple cameras are connected
camera = cv2.VideoCapture(0)
blurry = 0
counter = 0
blur_pass = False
# threshold for var of lap--to be tuned based on image capture conditions and requirements
thres = 5

print("Starting camera blurriness test...")

while blur_pass != True:
	ret, frame = camera.read()	

	# buffer image to be read and deleted
	img_name = "buffer-frame.png"
	cv2.imwrite(img_name, frame)

	# convert to grayscale then calculate var of laplacian
	image = cv2.imread('buffer-frame.png')
	gs = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
	fm = var_lap(gs)
	text = "Not Blurry"

	if fm < thres:
		text = "Blurry"
		blurry = 1

	# Overlay blurriness values (Remove if don't want to show person text overlayed)
	cv2.putText(image, "{}: {:.2f}".format(text, fm), (10, 30),
	cv2.FONT_ITALIC, 0.8, (0, 255, 0), 3)

	# Display Image
	cv2.imshow("Image", image)
	cv2.waitKey(50)


	# Check for user input on if image is clear
	pass_test = input("Was the image clear? (Y/N)")
	if (pass_test=='Y') and (blurry == 0):
		counter = counter+1
		if counter == 5: 
			blur_pass = True
		print ("Pass counter = ",counter,".")
	else:
		print ("Image deemed blurry. Adjust and retry")
		print ("Current Pass Counter = ",counter,".")


	blurry = 0 

	os.remove("buffer-frame.png")

# Instructions upon completion (, i.e. mark camera lens position or glue camera-lens assembly in place)
print ("Do X, Y, and/or Z as the camera has now been verified.")


camera.release()
cv2.destroyAllWindows()