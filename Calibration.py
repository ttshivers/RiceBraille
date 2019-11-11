# Import necessary packages
import numpy as np
import cv2 as cv
import ar_markers as ar
from ar_markers.marker import HammingMarker

# def getPaperCoordinates(markers):
#     for marker in markers:


test_image = cv.imread("images/CalibrationTestImage4.jpg")

markers = ar.detect_markers(test_image)
print(markers)
for marker in markers:
    marker.highlite_marker(test_image)

cv.imwrite('images/CalibrationTestImage4_marked.jpg', test_image)
# cv.imshow('test_image', test_image)
# cv.waitKey(0)
# cv.destroyAllWindows()

