from numpy.lib.type_check import imag
from image import Image
import glob
import cv2
import numpy as np


def myfunc(x):
    m = x.split("image")[-1]
    return int(m.split(".")[0])


def allImagesInThisDirectory(directory):
    list_of_possible_formats = [
        "bmp",
        "pbm",
        "pgm",
        "ppm",
        "sr",
        "ras",
        "jpeg",
        "jpg",
        "jpe",
        "jp2",
        "tiff",
        "tif",
        "png",
    ]
    list_of_images_directory = list()
    for format in list_of_possible_formats:
        list_of_images_directory += glob.glob(directory + "/*." + format)
    list_of_images_directory.sort(key=myfunc)
    list_of_image_objects = [Image(x) for x in list_of_images_directory]
    return list_of_image_objects


def allImagesInThisDirectory2(directory):
    list_of_possible_formats = [
        "bmp",
        "pbm",
        "pgm",
        "ppm",
        "sr",
        "ras",
        "jpeg",
        "jpg",
        "jpe",
        "jp2",
        "tiff",
        "tif",
        "png",
    ]
    list_of_images_directory = list()
    for format in list_of_possible_formats:
        list_of_images_directory += glob.glob(directory + "/*." + format)
    return list_of_images_directory


# now let's initialize the list of reference point
cropping = False
x_start, y_start, x_end, y_end = 0, 0, 0, 0
croped = None


def eazyCrop(image):
    def mouse_crop(event, x, y, flags, param):
        # grab references to the global variables
        global x_start, y_start, x_end, y_end, cropping, croped

        # if the left mouse button was DOWN, start RECORDING
        # (x, y) coordinates and indicate that cropping is being
        if event == cv2.EVENT_LBUTTONDOWN:
            x_start, y_start, x_end, y_end = x, y, x, y
            cropping = True

        # Mouse is Moving
        elif event == cv2.EVENT_MOUSEMOVE:
            if cropping == True:
                x_end, y_end = x, y

        # if the left mouse button was released
        elif event == cv2.EVENT_LBUTTONUP:
            # record the ending (x, y) coordinates
            x_end, y_end = x, y
            cropping = False  # cropping is finished
            refPoint = [(x_start, y_start), (x_end, y_end)]
            cv2.rectangle(image, (x_start, y_start), (x_end, y_end), (255, 0, 255), 1)
            if len(refPoint) == 2:  # when two points were found
                croped = image[
                    min(refPoint[0][1], refPoint[1][1])
                    + 1 : max(refPoint[0][1], refPoint[1][1]),
                    min(refPoint[0][0], refPoint[1][0])
                    + 1 : max(refPoint[0][0], refPoint[1][0]),
                ]

    # load the image, clone it, and setup the mouse callback function
    original = image.copy()
    image = image.copy()
    clone = image.copy()
    cv2.namedWindow("image")
    cv2.setMouseCallback("image", mouse_crop)

    # keep looping until the 'q' key is pressed
    while True:
        # display the image and wait for a keypress
        clone = image.copy()
        if not cropping:
            cv2.imshow("image", image)
        elif cropping:
            cv2.rectangle(clone, (x_start, y_start), (x_end, y_end), (255, 0, 255), 2)
            cv2.imshow("image", clone)

        key = cv2.waitKey(1) & 0xFF

        # press 'r' to reset the window
        if key == ord("r"):
            image = original.copy()

        # if the 'c' key is pressed, break from the loop
        elif key == ord("c"):
            return croped


ref_point = []
total_texts = []


def label(image):
    original = image.copy()

    def mouse_crop(event, x, y, flags, param):
        # grab references to the global variables
        global total_texts, x_start, y_start, x_end, y_end, cropping, croped, ref_point

        # if the left mouse button was DOWN, start RECORDING
        # (x, y) coordinates and indicate that cropping is being
        if event == cv2.EVENT_LBUTTONDOWN:
            x_start, y_start, x_end, y_end = x, y, x, y
            cropping = True

        # Mouse is Moving
        elif event == cv2.EVENT_MOUSEMOVE:
            if cropping == True:
                x_end, y_end = x, y

        # if the left mouse button was released
        elif event == cv2.EVENT_LBUTTONUP:
            # record the ending (x, y) coordinates
            x_end, y_end = x, y
            cropping = False  # cropping is finished
            refPoint = [(x_start, y_start), (x_end, y_end)]
            cv2.rectangle(image, (x_start, y_start), (x_end, y_end), (255, 0, 255), 1)
            if len(refPoint) == 2:
                x = min(refPoint[0][0], refPoint[1][0]) + 1
                y = min(refPoint[0][1], refPoint[1][1]) + 15
                text = input("Please enter the text:")
                total_texts.append(text)
                cv2.putText(
                    image,
                    text,
                    (x, y),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    0.5,
                    (255, 0, 120),
                    2,
                )
                ref_point.append(refPoint)

    # grab references to the global variables
    global total_texts, ref_point
    ref_point.clear()
    total_texts.clear()
    # load the image, clone it, and setup the mouse callback function
    clone = image.copy()
    cv2.namedWindow("image")
    cv2.setMouseCallback("image", mouse_crop)

    while True:
        # display the image and wait for a keypress
        clone = image.copy()
        if not cropping:
            cv2.imshow("image", image)
        elif cropping:
            cv2.rectangle(clone, (x_start, y_start), (x_end, y_end), (255, 0, 255), 2)
            cv2.imshow("image", clone)

        key = cv2.waitKey(1) & 0xFF
        # press 'r' to reset the window
        if key == ord("r"):
            image = original.copy()
            ref_point.clear()
            total_texts.clear()

        # if the 'e' key is pressed, break from the loop
        elif key == ord("e"):
            image = original.copy()
            cv2.destroyAllWindows()
            return [clone, ref_point, total_texts]


def rotate(origin, point, angle):
    ox, oy = origin
    px, py = point
    angle = np.radians(angle)
    qx = ox + np.cos(angle) * (px - ox) - np.sin(angle) * (py - oy)
    qy = oy + np.sin(angle) * (px - ox) + np.cos(angle) * (py - oy)
    return int(qx), int(qy)


# print(rotate((0,900),(1200,0),-180))
# print(rotate((0,900),(1200,0),-180))
# print(rotate((,900),(1200,0),-180))
# print(rotate((0,900),(1200,0),-180))
