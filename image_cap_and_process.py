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
# threshold for var of lap--to be tuned based on image capture conditions and requirements
thres = 100

while True:
	ret, frame = camera.read()	

	# buffer image to be read and deleted
	img_name = "buffer-frame.png"
	cv2.imwrite(img_name, frame)
	print("{} written!".format(img_name))

	# convert to grayscale then calculate var of laplacian
	image = cv2.imread('buffer-frame.png')
	gs = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
	fm = var_lap(gs)
	text = "Not Blurry"

	if fm < thres:
		text = "Blurry"

	# Overlay blurriness values
	cv2.putText(image, "{}: {:.2f}".format(text, fm), (10, 30),
	cv2.FONT_ITALIC, 0.8, (0, 0, 255), 3)
	cv2.imshow("Image", image)
	cv2.waitKey(0)

	os.remove("buffer-frame.png")

camera.release()
cv2.destroyAllWindows()