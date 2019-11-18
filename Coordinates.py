# Import necessary packages
import numpy as np
import cv2 as cv
import ar_markers as ar


def getPaperCoordinates(coordinates, markers):
    horizontalDist = 400
    verticalDist = 600

    for marker in markers:
        if marker.id == 2226:
            top_left = marker.center
        if marker.id == 2265:
            top_right = marker.center
        if marker.id == 2023:
            bottom_left = marker.center
        if marker.id == 2421:
            bottom_right = marker.center

    print(top_left)
    print(top_right)
    print(bottom_left)
    print(bottom_right)
    a = top_right[0] - top_left[0]
    b = bottom_right[0] - bottom_left[0]
    c = bottom_left[1] - top_left[1]
    d = bottom_right[1] - top_right[1]
    print(a, b, c, d)
    x1 = coordinates[0] / a * horizontalDist
    x2 = coordinates[0] / b * horizontalDist
    y1 = coordinates[1] / c * verticalDist
    y2 = coordinates[1] / d * verticalDist
    print(x1, x2, y1, y2)

    return (int(np.mean([x1, x2])), int(np.mean([y1, y2])))


test_image = cv.imread("images/Scanned_Collin.jpg")


markers = ar.detect_markers(test_image)
print(test_image.shape)
print(markers)
for marker in markers:
    marker.highlite_marker(test_image)

print()
test_point = (300, 400)
cv.circle(test_image, test_point, 10, (255, 0, 0))

point = getPaperCoordinates(test_point, markers)
print(point)
cv.circle(test_image, point, 10, (0, 255, 0))

cv.imshow('test_image', test_image)
cv.waitKey(0)
cv.destroyAllWindows()

