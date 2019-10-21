# import the necessary packages
import numpy as np
import argparse
import cv2 as cv

# construct the argument parse and parse the arguments
ap = argparse.ArgumentParser()
ap.add_argument("-i", "--image", help="path to the image")
args = vars(ap.parse_args())

# load the image
image = cv.imread("eight.jpg")
cv.namedWindow("Display Window", cv.WINDOW_AUTOSIZE)
# Take each frame
# Convert BGR to HSV
hsv = cv.cvtColor(image, cv.COLOR_BGR2HSV)
# define range of blue color in HSV
delta = 2.5
lower_green = np.array([50 - delta, 100, 100])
upper_green = np.array([50 + delta, 255, 255])

lower_blue = np.array([100 - delta, 100, 100])
upper_blue = np.array([100 + delta, 255, 255])

lower_pink = np.array([166 - delta, 100, 100])
upper_pink = np.array([166 + delta, 255, 255])

lower_purple = np.array([130 - delta, 0, 0])
upper_purple = np.array([130 + delta, 255, 255])

lower_yellow = np.array([28 - delta, 0, 0])
upper_yellow = np.array([28 + delta, 255, 255])

# Threshold the HSV image to get only blue colors
# Threshold the HSV image to get only green colors
mask_green = cv.inRange(hsv, lower_green, upper_green)
# Threshold for blue
mask_blue = cv.inRange(hsv, lower_blue, upper_blue)
mask_pink = cv.inRange(hsv, lower_pink, upper_pink)
mask_purple = cv.inRange(hsv, lower_purple, upper_purple)
mask_yellow = cv.inRange(hsv, lower_yellow, upper_yellow)


# Bitwise-AND mask and original image
res = cv.bitwise_and(image, image, mask=(mask_green | mask_blue | mask_pink | mask_purple | mask_yellow))
print(image.shape)
cv.imwrite("original.jpg", image)
cv.imwrite("mask.jpg", mask_blue)
cv.imwrite("res.jpg", res)
'''
cv.imshow('Display Window', image)
cv.waitKey(0)
cv.imshow('mask', mask)
cv.waitKey(0)
cv.imshow('res', res)
cv.waitKey(0)
'''


