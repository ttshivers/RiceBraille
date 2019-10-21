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

def set_masks(colors, delta):
    bounds = [(np.array([color - delta, 100, 100]), np.array([color + delta, 255, 255])) for color in colors]
    masks = [cv.inRange(hsv, bound[0], bound[1]) for bound in bounds]
    mask = masks[0]
    for i in range(1, len(masks)):
        mask = mask | masks[i]
    return mask

colors = [46, 100, 166, 130, 28, 146]
delta = 10
colormask = set_masks(colors, delta)


# Bitwise-AND mask and original image
res = cv.bitwise_and(image, image, mask=colormask)
print(image.shape)
cv.imwrite("original.jpg", image)
cv.imwrite("res2.jpg", res)
'''
cv.imshow('Display Window', image)
cv.waitKey(0)
cv.imshow('mask', mask)
cv.waitKey(0)
cv.imshow('res', res)
cv.waitKey(0)
'''


