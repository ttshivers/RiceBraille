# Import necessary packages
import numpy as np
import cv2 as cv
import ar_markers as ar
#import qrtools
# from qrtools.qrtools import QR
# from ar_markers.marker import HammingMarker


# test_image = cv.imread("images/coordinateTransformDots4Perspective.jpg")
#
# markers = ar.detect_markers(test_image)
# print(test_image.shape)
# print(markers)
# for marker in markers:
#     marker.highlite_marker(test_image)
#
# cv.imwrite('images/calibrationCoordinateTestDots4.jpg', test_image)
#
#
# Display barcode and QR code location
def display(im, bbox):
    n = len(bbox)
    for j in range(n):
        cv.line(im, tuple(bbox[j][0]), tuple(bbox[(j + 1) % n][0]), (255, 0, 0), 3)

    # Display results
    cv.imshow("Results", im)


# qr = qrtools.QR()
# qr.decode("hooplah")

# creates the QR object
# my_QR = QR(data=u"hooplah")
#
# # encodes to a QR code
# my_QR.encode()

qr_image1 = cv.imread("images/qr_code_fullpage_test2.jpg")
qr_image2 = cv.imread("images/QRcodeTest1.jpg")
qr_image = cv.imread("images/qr_code_test8.jpg")
print(qr_image1.shape)
print(qr_image2.shape)
print(qr_image.shape)

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



