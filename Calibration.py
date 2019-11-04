# Import necessary packages
import numpy as np
import cv2 as cv
import ar_markers as ar
from ar_markers.marker import HammingMarker



test_image = cv.imread("images/armarkerCornerPresentResult.jpg")

markers = ar.detect_markers(test_image)
print(test_image.shape)
print(markers)
for marker in markers:
    marker.highlite_marker(test_image)

cv.imwrite('images/armarkerCorner.jpg', test_image)
# cv.imshow('test_image', test_image)
# cv.waitKey(0)
# cv.destroyAllWindows()

