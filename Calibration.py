# Import necessary packages
import numpy as np
import cv2 as cv
import ar_markers as ar
from ar_markers.marker import HammingMarker


test_image = cv.imread("images/coordinateTransformDots4Perspective.jpg")

markers = ar.detect_markers(test_image)
print(test_image.shape)
print(markers)
for marker in markers:
    marker.highlite_marker(test_image)

cv.imwrite('images/calibrationCoordinateTestDots4.jpg', test_image)


# Display barcode and QR code location
def display(im, bbox):
    n = len(bbox)
    for j in range(n):
        cv.line(im, tuple(bbox[j][0]), tuple(bbox[(j + 1) % n][0]), (255, 0, 0), 3)

    # Display results
    cv.imshow("Results", im)


qr_image = cv.imread("images/QR_code_test2.jpg")
qrDecoder = cv.QRCodeDetector()

data, bbox, rectifiedImage = qrDecoder.detectAndDecode(qr_image)
if len(data) > 0:
    print("Decoded Data : {}".format(data))
    display(qr_image, bbox)
    rectifiedImage = np.uint8(rectifiedImage);
    cv.imwrite("images/qr_code_test2_result.jpg", rectifiedImage);
else:
    print("QR Code not detected")
    cv.imwrite("images/qr_code_test2_result.jpg", qr_image)
cv.waitKey(0)
cv.destroyAllWindows()

# cv.imshow('test_image', test_image)
# cv.waitKey(0)
# cv.destroyAllWindows()
