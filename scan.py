# USAGE
# python scan.py --image images/page.jpg

# import the necessary packages
from pyimagesearch.transform import four_point_transform
from skimage.filters import threshold_local
import ar_markers as ar
import cv2
import imutils
import numpy as np


def transform_image(image_file, paper_dims=(425, 550), output_image="scannedImage.jpg"):
    """
    :param image_file: name of image to read from
    :param paper_dims: dimensions of paper (in pixels) to scale scanned image to
    :param output_image: name of file to write new image to
    :return: returns transformation matrix
    """
    # load the image and compute the ratio of the old height
    # to the new height, clone it, and resize it
    image = cv2.imread(image_file)
    ratio = image.shape[0] / 500.0
    orig = image.copy()
    image = imutils.resize(image, height=500)

    # convert the image to grayscale, blur it, and find edges
    # in the image
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    gray = cv2.GaussianBlur(gray, (5, 5), 0)
    edged = cv2.Canny(gray, 75, 200)

    # show the original image and the edge detected image
    print("STEP 1: Edge Detection")
    cv2.imshow("Image", image)
    cv2.imshow("Edged", edged)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

    # find the contours in the edged image, keeping only the
    # largest ones, and initialize the screen contour
    cnts = cv2.findContours(edged.copy(), cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)
    cnts = imutils.grab_contours(cnts)
    cnts = sorted(cnts, key=cv2.contourArea, reverse=True)[:5]

    # loop over the contours
    for c in cnts:
        # approximate the contour
        peri = cv2.arcLength(c, True)
        approx = cv2.approxPolyDP(c, 0.02 * peri, True)

        # if our approximated contour has four points, then we
        # can assume that we have found our screen
        if len(approx) == 4:
            screenCnt = approx
            break

    # show the contour (outline) of the piece of paper
    print("STEP 2: Find contours of paper")
    cv2.drawContours(image, [screenCnt], -1, (0, 255, 0), 2)
    cv2.imshow("Outline", image)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

    # apply the four point transform to obtain a top-down
    # view of the original image
    M, warped = four_point_transform(orig, screenCnt.reshape(4, 2) * ratio)

    # convert the warped image to grayscale, then threshold it
    # to give it that 'black and white' paper effect
    # warped = cv2.cvtColor(warped, cv2.COLOR_BGR2GRAY)
    # T = threshold_local(warped, 11, offset=10, method="gaussian")
    # warped = (warped > T).astype("uint8") * 255

    # show the original and scanned images
    print("STEP 3: Apply perspective transform")
    if paper_dims == None:
        cv2.imwrite(output_image, imutils.resize(warped, height=650))
        cv2.imshow("Original", imutils.resize(orig, height=650))
        cv2.imshow("Scanned", imutils.resize(warped, height=650))
    else:
        cv2.imwrite(output_image, cv2.resize(warped, paper_dims))
        cv2.imshow("Scanned", cv2.resize(warped, paper_dims))
    cv2.waitKey(0)

    return M


def find_markers(image_file, output_image="markers.jpg"):
    """
    :param image_file: filename to read from
    :param output_image: name of file to write new images to
    """
    test_image = cv2.imread(image_file)

    markers = ar.detect_markers(test_image)
    print(test_image.shape)
    print(markers)
    for marker in markers:
        marker.highlite_marker(test_image)
    cv2.imshow("Markers", test_image)
    cv2.waitKey(0)
    cv2.imwrite(output_image, test_image)


def transform_and_markers(image_file, paper_dims=(425, 550), scanned_output="scanned.jpg", final_output="scannedMarkers.jpg"):
    """
    :param image_file: original image file to read from
    :param paper_dims: paper dims to scale to (as used in transform image)
    :param scanned_output: output file for image that is scanned but does not have ar markers detected yet
    :param final_output: file name for image with ar markers detect
    """
    transform_image(image_file, paper_dims, scanned_output)
    find_markers(scanned_output, final_output)

def transform_point(point: [int, int], M):
    """
    :param point: point in original plane
    :param M: transformation matrix
    :return: prints point that point is transformed to in new plane
    """
    a = np.array([point], dtype='float32')
    a = np.array([a])
    print(cv2.perspectiveTransform(a, M))


#transform_and_markers("images/arFour.jpg")
my_mat = transform_image("images/arFour.jpg")
transform_point([0, 0], my_mat)
