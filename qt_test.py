import os
import shutil
import sys
from typing import Counter
from PyQt5.QtGui import QColor, QFont, QStandardItemModel, QStandardItem, QIcon, QPixmap
import numpy as np
from PyQt5.QtWidgets import (
    QFileDialog,
    QGraphicsDropShadowEffect,
    QMainWindow,
    QApplication,
    QVBoxLayout,
    QDialog,
    QTreeWidgetItem,
    QTreeView,
)
from PyQt5 import uic, QtCore, QtWidgets, QtGui
from PyQt5.QtCore import Qt, QRect
from PyQt5.Qt import QStandardItemModel
import matplotlib
import random

matplotlib.use("Qt5Agg")
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT as NavigationToolbar
from matplotlib.figure import Figure
from time import sleep
from image import Image
from funcs import allImagesInThisDirectory, allImagesInThisDirectory2, rotate, label
import cv2


my_form_SplashScreen = uic.loadUiType(os.path.join(os.getcwd(), "first.ui"))[0]
my_form_main = uic.loadUiType(os.path.join(os.getcwd(), "main.ui"))[0]
my_form_flip = uic.loadUiType(os.path.join(os.getcwd(), "flipWindow.ui"))[0]
my_form_brightness = uic.loadUiType(os.path.join(os.getcwd(), "brightnessWindow.ui"))[0]
my_form_rotation = uic.loadUiType(os.path.join(os.getcwd(), "rotationWindow.ui"))[0]
my_form_noise = uic.loadUiType(os.path.join(os.getcwd(), "noiseWindow.ui"))[0]
my_form_blurring = uic.loadUiType(os.path.join(os.getcwd(), "blurringWindow.ui"))[0]
my_form_crop = uic.loadUiType(os.path.join(os.getcwd(), "cropWindow.ui"))[0]
my_form_upload = uic.loadUiType(os.path.join(os.getcwd(), "uploadWindow.ui"))[0]
my_form_tag = uic.loadUiType(os.path.join(os.getcwd(), "taggingWindow.ui"))[0]
my_form_split = uic.loadUiType(os.path.join(os.getcwd(), "splitWindow.ui"))[0]
my_form_filtering = uic.loadUiType(os.path.join(os.getcwd(), "filteringWindow.ui"))[0]
my_form_resize = uic.loadUiType(os.path.join(os.getcwd(), "resizeWindow.ui"))[0]
my_form_fast = uic.loadUiType(os.path.join(os.getcwd(), "fastWindow.ui"))[0]


##global
Counter = 0
# Uploading
class UploadWindow(QMainWindow, my_form_upload):
    _count = 0

    def __init__(self):
        super(UploadWindow, self).__init__()
        self.setupUi(self)
        self.setWindowTitle("Upload")
        self.browse.clicked.connect(self.browseImages)
        self.setWindowFlag(QtCore.Qt.FramelessWindowHint)
        self.setAttribute(QtCore.Qt.WA_TranslucentBackground)
        self.pushButton_4.clicked.connect(self.exit)
        self.setFixedSize(676, 276)

    def exit(self):
        self.close()

    def browseImages(self):
        imagePath = QFileDialog.getExistingDirectory(self, "Select file")
        list_of_images_directory = allImagesInThisDirectory2(imagePath)
        l = len(list_of_images_directory)
        if l == 0:
            self.label.setText("There is no image here!")
        else:
            for i in range(l):
                UploadWindow._count += 1
                name = str(UploadWindow._count)
                pixmap = QPixmap(list_of_images_directory[i])
                # pixmap = pixmap.scaled(600, 450)
                pixmap.save(".\images\image" + name + ".jpg")
            selectedImage = QPixmap(list_of_images_directory[0])
            selectedImage = selectedImage.scaled(600, 450)
            selectedImage.save("2.jpg")
            selectedImage = selectedImage.scaled(240, 180)
            selectedImage.save("1.jpeg")
            selectedImage.save("1.jpg")
            self.label.setText("<strong>Successfully Uploaded!</strong>")


## flip window
class FlipWindow(QMainWindow, my_form_flip):
    def __init__(self):
        super(FlipWindow, self).__init__()
        self.setupUi(self)
        self.setWindowTitle("Flip")
        # remove title bar
        self.setWindowFlag(QtCore.Qt.FramelessWindowHint)
        self.setAttribute(QtCore.Qt.WA_TranslucentBackground)

        self.imagename = "1"
        self.imagename = str(
            np.clip(int(self.imagename), None, UploadWindow._count - 1) + 1
        )
        pixmap = QPixmap("./images/image" + self.imagename + ".jpg")
        pixmap = pixmap.scaled(550, 350)
        self.label_original_image.setPixmap(pixmap)
        self.label_original_image.setAlignment(QtCore.Qt.AlignCenter)

        # self.checkBox_h.stateChanged.connect(self.state_changed)
        # self.checkBox_v.stateChanged.connect(self.state_changed)
        self.pushButton.clicked.connect(self.state_changed)
        self.pushButton_4.clicked.connect(self.exit)
        self.pushButton_5.clicked.connect(self.applyToAll)
        self.setFixedSize(1045, 700)

    def exit(self):
        self.close()

    def state_changed(self, int):

        src = cv2.imread("1.jpg")
        imgObject = Image("./images/image" + self.imagename + ".jpg")
        image = cv2.resize(imgObject.img, (550, 350))
        cv2.imwrite("my.jpg", image)
        src = cv2.imread("my.jpg")

        if not (self.checkBox_h.isChecked() & self.checkBox_v.isChecked()):
            self.label_fliped_image.setText(" ")

        if self.checkBox_h.isChecked() & self.checkBox_v.isChecked():
            img = cv2.flip(src, -1)
            cv2.imwrite("my.png", img)
            pixmap = QtGui.QPixmap("my.png")
            self.label_fliped_image.setPixmap(pixmap)
            self.label_fliped_image.show()

        elif self.checkBox_v.isChecked():
            img = cv2.flip(src, 0)
            cv2.imwrite("my.png", img)
            pixmap = QtGui.QPixmap("my.png")
            self.label_fliped_image.setPixmap(pixmap)
            self.label_fliped_image.show()
        elif self.checkBox_h.isChecked():
            img = cv2.flip(src, 1)
            cv2.imwrite("my.png", img)
            pixmap = QtGui.QPixmap("my.png")
            self.label_fliped_image.setPixmap(pixmap)
            self.label_fliped_image.show()

    def applyToAll(self):
        my_list = allImagesInThisDirectory("./images")
        t = 0
        for src in my_list:
            t += 1
            UploadWindow._count += 1
            if self.checkBox_h.isChecked() and self.checkBox_v.isChecked():
                img = cv2.flip(src.img, -1)
                mode = "b"
                cv2.imwrite(".\images\image" + str(UploadWindow._count) + ".jpg", img)

            elif self.checkBox_v.isChecked():
                img = cv2.flip(src.img, 0)
                mode = "v"
                cv2.imwrite(".\images\image" + str(UploadWindow._count) + ".jpg", img)
            elif self.checkBox_h.isChecked():
                img = cv2.flip(src.img, 1)
                mode = "h"
                cv2.imwrite(".\images\image" + str(UploadWindow._count) + ".jpg", img)
            if os.path.isfile("./tagged/ref_pointsOfimage" + str(t) + ".txt"):
                file1 = open("./tagged/ref_pointsOfimage" + str(t) + ".txt", "r")
                lines = file1.read().split("\n")
                file1.close()
                for line in lines:
                    if line == "":
                        continue
                    points, text = line.split("->")
                    x0, y0, xp0, yp0 = points.split(",")
                    x0, y0, xp0, yp0 = int(x0), int(y0), int(xp0), int(yp0)
                    if mode == "h":
                        x0 = len(img[0]) - x0
                        xp0 = len(img[0]) - xp0
                    if mode == "v":
                        y0 = len(img) - y0
                        yp0 = len(img) - yp0
                    if mode == "b":
                        y0 = len(img) - y0
                        yp0 = len(img) - yp0
                        x0 = len(img[0]) - x0
                        xp0 = len(img[0]) - xp0
                    xmin = min(x0, xp0)
                    ymin = min(y0, yp0)
                    xmax = max(x0, xp0)
                    ymax = max(y0, yp0)
                    file1 = open(
                        "./tagged/ref_pointsOfimage"
                        + str(UploadWindow._count)
                        + ".txt",
                        "a",
                    )
                    file1.write(
                        str(xmin)
                        + ","
                        + str(ymin)
                        + ","
                        + str(xmax)
                        + ","
                        + str(ymax)
                        + "->"
                        + text
                        + "\n"
                    )
                    file1.close()


## resize window
class ResizeWindow(QMainWindow, my_form_resize):
    def __init__(self):
        super(ResizeWindow, self).__init__()
        self.setupUi(self)
        self.setWindowTitle("Resize")
        # remove title bar
        self.setWindowFlag(QtCore.Qt.FramelessWindowHint)
        self.setAttribute(QtCore.Qt.WA_TranslucentBackground)

        self.imagename = "1"
        self.imagename = str(
            np.clip(int(self.imagename), None, UploadWindow._count - 1) + 1
        )
        pixmap = QPixmap("./images/image" + self.imagename + ".jpg")
        pixmap = pixmap.scaled(550, 350)
        self.label_original_image.setPixmap(pixmap)
        self.label_original_image.setAlignment(QtCore.Qt.AlignCenter)

        self.pushButton.clicked.connect(self.state_changed)
        self.pushButton_4.clicked.connect(self.exit)
        self.pushButton_5.clicked.connect(self.applyToAll)
        self.setFixedSize(1000, 700)

    def exit(self):
        self.close()

    def state_changed(self, int):
        h = np.int64(float(self.height.text()))
        w = np.int64(float(self.width.text()))

        # resize image
        imgObject = Image("./images/image" + self.imagename + ".jpg")
        image = cv2.resize(imgObject.img, (550, 350))

        im = cv2.imwrite("my.jpg", image)
        src = cv2.imread("my.jpg")
        height = np.int(src.shape[0] * h / 100)
        width = np.int(src.shape[1] * w / 100)
        dim = (width, height)

        img = cv2.resize(src, dim, interpolation=cv2.INTER_AREA)
        cv2.imwrite("my.png", img)
        pixmap = QtGui.QPixmap("my.png")
        self.label_resized_image.setPixmap(pixmap)
        self.label_resized_image.setAlignment(QtCore.Qt.AlignCenter)
        self.label_resized_image.show()

    def applyToAll(self):
        my_list = allImagesInThisDirectory("./images")
        t = 0
        for src in my_list:
            # img = cv2.flip(src.img, -1)
            h = np.int64(float(self.height.text()))
            w = np.int64(float(self.width.text()))
            height = np.int64(src.img.shape[0] * h / 100)
            width = np.int64(src.img.shape[1] * w / 100)
            dim = (width, height)
            img = cv2.resize(src.img, dim, interpolation=cv2.INTER_AREA)
            UploadWindow._count += 1
            cv2.imwrite(".\images\image" + str(UploadWindow._count) + ".jpg", img)

            t += 1
            if os.path.isfile("./tagged/ref_pointsOfimage" + str(t) + ".txt"):
                file1 = open("./tagged/ref_pointsOfimage" + str(t) + ".txt", "r")
                lines = file1.read().split("\n")
                file1.close()
                for line in lines:
                    if line == "":
                        continue
                    points, text = line.split("->")
                    x0, y0, xp0, yp0 = points.split(",")
                    x1 = int(x0) * w // 100
                    x2 = int(xp0) * w // 100
                    y1 = int(y0) * h // 100
                    y2 = int(yp0) * h // 100
                    xmin = min(x2, x1)
                    ymin = min(y2, y1)
                    xmax = max(x2, x1)
                    ymax = max(y2, y1)
                    file1 = open(
                        "./tagged/ref_pointsOfimage"
                        + str(UploadWindow._count)
                        + ".txt",
                        "a",
                    )
                    file1.write(
                        str(x1)
                        + ","
                        + str(y1)
                        + ","
                        + str(x2)
                        + ","
                        + str(y2)
                        + "->"
                        + text
                        + "\n"
                    )
                    file1.close()


# brightness window
class BrightnessWindow(QMainWindow, my_form_brightness):
    def __init__(self):
        super(BrightnessWindow, self).__init__()
        self.setupUi(self)
        self.setWindowTitle("Brightness")
        self.horizontalSlider.valueChanged.connect(self.state_changed)
        # remove title bar
        self.setWindowFlag(QtCore.Qt.FramelessWindowHint)
        self.setAttribute(QtCore.Qt.WA_TranslucentBackground)
        self.pushButton_4.clicked.connect(self.exit)
        self.pushButton_5.clicked.connect(self.applyToAll)
        self.setFixedSize(666, 828)

    def applyToAll(self):
        my_list = allImagesInThisDirectory("./images")
        t = 0
        for img in my_list:
            t += 1
            ans = img.adjustBrightness(self.int / 100)
            UploadWindow._count += 1
            cv2.imwrite(".\images\image" + str(UploadWindow._count) + ".jpg", ans)
            if os.path.isfile("./tagged/ref_pointsOfimage" + str(t) + ".txt"):
                file1 = open("./tagged/ref_pointsOfimage" + str(t) + ".txt", "r")
                lines = file1.read().split("\n")
                file1.close()
                for line in lines:
                    if line == "":
                        continue
                    points, text = line.split("->")
                    x0, y0, xp0, yp0 = points.split(",")
                    x0, y0, xp0, yp0 = int(x0), int(y0), int(xp0), int(yp0)
                    xmin = min(x0, xp0)
                    ymin = min(y0, yp0)
                    xmax = max(x0, xp0)
                    ymax = max(y0, yp0)
                    file1 = open(
                        "./tagged/ref_pointsOfimage"
                        + str(UploadWindow._count)
                        + ".txt",
                        "a",
                    )
                    file1.write(
                        str(xmin)
                        + ","
                        + str(ymin)
                        + ","
                        + str(xmax)
                        + ","
                        + str(ymax)
                        + "->"
                        + text
                        + "\n"
                    )
                    file1.close()

    def exit(self):
        self.close()

    def state_changed(self, int):
        self.int = int
        imgObject = Image("2.jpg")
        img = imgObject.adjustBrightness(int / 100)
        cv2.imwrite("ui.jpg", img)
        pixmap = QPixmap("ui.jpg")
        self.label.setPixmap(pixmap)


# rotation window
class RotationWindow(QMainWindow, my_form_rotation):
    def __init__(self):
        super(RotationWindow, self).__init__()
        self.setupUi(self)
        self.setWindowTitle("rotation")
        self.horizontalSlider.valueChanged.connect(self.state_changed)
        # remove title bar
        self.setWindowFlag(QtCore.Qt.FramelessWindowHint)
        self.setAttribute(QtCore.Qt.WA_TranslucentBackground)
        self.pushButton_7.clicked.connect(self.exit)
        self.pushButton_8.clicked.connect(self.applyToAll)
        self.setFixedSize(666, 828)

    def applyToAll(self):
        my_list = allImagesInThisDirectory("./images")
        t = 0
        for img in my_list:
            t += 1
            origin = (((len(img.img[0]) - 1) // 2), ((len(img.img) - 1) // 2))
            ans = img.rotate(-self.int)
            UploadWindow._count += 1
            cv2.imwrite(".\images\image" + str(UploadWindow._count) + ".jpg", ans)
            if os.path.isfile("./tagged/ref_pointsOfimage" + str(t) + ".txt"):
                file1 = open("./tagged/ref_pointsOfimage" + str(t) + ".txt", "r")
                lines = file1.read().split("\n")
                file1.close()
                for line in lines:
                    if line == "":
                        continue
                    points, text = line.split("->")
                    x0, y0, xp0, yp0 = points.split(",")
                    x1, y1 = rotate(origin, (int(x0), int(y0)), self.int)
                    x2, y2 = rotate(origin, (int(xp0), int(yp0)), self.int)
                    x3, y3 = rotate(origin, (int(x0), int(yp0)), self.int)
                    x4, y4 = rotate(origin, (int(xp0), int(y0)), self.int)
                    xmin = min(x1, x2, x3, x4)
                    ymin = min(y1, y2, y3, y4)
                    xmax = max(x1, x2, x3, x4)
                    ymax = max(y1, y2, y3, y4)
                    if xmin < 0:
                        xmin = 0
                    if ymin < 0:
                        ymin = 0
                    if xmax >= len(img.img[0]):
                        xmax = len(img.img[0]) - 1
                    if ymax >= len(img.img):
                        ymax = len(img.img) - 1
                    file1 = open(
                        "./tagged/ref_pointsOfimage"
                        + str(UploadWindow._count)
                        + ".txt",
                        "a",
                    )
                    file1.write(
                        str(xmin)
                        + ","
                        + str(ymin)
                        + ","
                        + str(xmax)
                        + ","
                        + str(ymax)
                        + "->"
                        + text
                        + "\n"
                    )
                    file1.close()

    def exit(self):
        self.close()

    def state_changed(self, int):
        self.int = int
        imgObject = Image("2.jpg")
        img = imgObject.rotate(-int)
        cv2.imwrite("ui.jpg", img)
        pixmap = QPixmap("ui.jpg")
        self.label.setPixmap(pixmap)


# noise window
class NoiseWindow(QMainWindow, my_form_noise):
    def __init__(self):
        super(NoiseWindow, self).__init__()
        self.setupUi(self)
        self.setWindowTitle("noise")
        self.mode = None
        self.horizontalSlider.hide()
        self.horizontalSlider.valueChanged.connect(self.state_changed)
        self.pushButton.clicked.connect(self.gauss)
        self.pushButton_2.clicked.connect(self.speckle)
        self.pushButton_3.clicked.connect(self.poisson)
        self.pushButton_4.clicked.connect(self.salt)
        self.pushButton_5.clicked.connect(self.pepper)
        self.pushButton_6.clicked.connect(self.sp)
        # remove title bar
        self.setWindowFlag(QtCore.Qt.FramelessWindowHint)
        self.setAttribute(QtCore.Qt.WA_TranslucentBackground)
        self.pushButton_7.clicked.connect(self.exit)
        self.pushButton_8.clicked.connect(self.applyToAll)
        self.setFixedSize(666, 828)

    def applyToAll(self):
        my_list = allImagesInThisDirectory("./images")
        t = 0
        for img in my_list:
            t += 1
            ans = img.addnoise(self.mode, self.int / 100)
            UploadWindow._count += 1
            cv2.imwrite(".\images\image" + str(UploadWindow._count) + ".jpg", ans)
            cv2.imwrite(".\images\image" + str(UploadWindow._count) + ".jpg", ans)
            if os.path.isfile("./tagged/ref_pointsOfimage" + str(t) + ".txt"):
                file1 = open("./tagged/ref_pointsOfimage" + str(t) + ".txt", "r")
                lines = file1.read().split("\n")
                file1.close()
                for line in lines:
                    if line == "":
                        continue
                    points, text = line.split("->")
                    x0, y0, xp0, yp0 = points.split(",")
                    x0, y0, xp0, yp0 = int(x0), int(y0), int(xp0), int(yp0)
                    xmin = min(x0, xp0)
                    ymin = min(y0, yp0)
                    xmax = max(x0, xp0)
                    ymax = max(y0, yp0)
                    file1 = open(
                        "./tagged/ref_pointsOfimage"
                        + str(UploadWindow._count)
                        + ".txt",
                        "a",
                    )
                    file1.write(
                        str(xmin)
                        + ","
                        + str(ymin)
                        + ","
                        + str(xmax)
                        + ","
                        + str(ymax)
                        + "->"
                        + text
                        + "\n"
                    )
                    file1.close()

    def exit(self):
        self.close()

    def gauss(self):
        self.mode = "gaussian"
        self.horizontalSlider.show()

    def speckle(self):
        self.mode = "speckle"
        self.horizontalSlider.show()

    def poisson(self):
        self.mode = "poisson"
        self.horizontalSlider.hide()
        imgObject = Image("2.jpg")
        img = imgObject.addnoise(self.mode)
        cv2.imwrite("ui.jpg", img)
        pixmap = QPixmap("ui.jpg")
        self.label.setPixmap(pixmap)

    def salt(self):
        self.mode = "salt"
        self.horizontalSlider.show()

    def pepper(self):
        self.mode = "pepper"
        self.horizontalSlider.show()

    def sp(self):
        self.mode = "s&p"
        self.horizontalSlider.show()

    def state_changed(self, int):
        imgObject = Image("2.jpg")
        self.int = int
        img = imgObject.addnoise(self.mode, int / 100)
        cv2.imwrite("ui.jpg", img)
        pixmap = QtGui.QPixmap("ui.jpg")
        self.label.setPixmap(pixmap)


# blurring window
class BlurringWindow(QMainWindow, my_form_blurring):
    def __init__(self):
        super(BlurringWindow, self).__init__()
        self.setupUi(self)
        self.setWindowTitle("blurring")
        self.mode = None
        self.horizontalSlider.hide()

        self.horizontalSlider.valueChanged.connect(self.state_changed)
        self.pushButton.clicked.connect(self.gauss)
        self.pushButton_2.clicked.connect(self.median)
        self.pushButton_3.clicked.connect(self.bilateral)
        self.pushButton_4.clicked.connect(self.exit)
        self.pushButton_5.clicked.connect(self.applyToAll)
        self.setFixedSize(666, 828)

        # remove title bar
        self.setWindowFlag(QtCore.Qt.FramelessWindowHint)
        self.setAttribute(QtCore.Qt.WA_TranslucentBackground)

    def applyToAll(self):
        my_list = allImagesInThisDirectory("./images")
        t = 0
        if self.int % 2 == 0:
            self.int += 1
        for img in my_list:
            t += 1
            if self.mode == "g":
                ans = cv2.GaussianBlur(img.img, (self.int, self.int), 0)
            elif self.mode == "m":
                ans = cv2.medianBlur(img.img, self.int)
            elif self.mode == "b":
                ans = cv2.bilateralFilter(img.img, self.int, 75, 75)
            UploadWindow._count += 1
            cv2.imwrite(".\images\image" + str(UploadWindow._count) + ".jpg", ans)
            cv2.imwrite(".\images\image" + str(UploadWindow._count) + ".jpg", ans)
            if os.path.isfile("./tagged/ref_pointsOfimage" + str(t) + ".txt"):
                file1 = open("./tagged/ref_pointsOfimage" + str(t) + ".txt", "r")
                lines = file1.read().split("\n")
                file1.close()
                for line in lines:
                    if line == "":
                        continue
                    points, text = line.split("->")
                    x0, y0, xp0, yp0 = points.split(",")
                    x0, y0, xp0, yp0 = int(x0), int(y0), int(xp0), int(yp0)
                    xmin = min(x0, xp0)
                    ymin = min(y0, yp0)
                    xmax = max(x0, xp0)
                    ymax = max(y0, yp0)
                    file1 = open(
                        "./tagged/ref_pointsOfimage"
                        + str(UploadWindow._count)
                        + ".txt",
                        "a",
                    )
                    file1.write(
                        str(xmin)
                        + ","
                        + str(ymin)
                        + ","
                        + str(xmax)
                        + ","
                        + str(ymax)
                        + "->"
                        + text
                        + "\n"
                    )
                    file1.close()

    def gauss(self):
        self.mode = "g"
        self.horizontalSlider.show()

    def median(self):
        self.mode = "m"
        self.horizontalSlider.show()

    def bilateral(self):
        self.mode = "b"
        self.horizontalSlider.show()

    def exit(self):
        self.close()

    def state_changed(self, int):
        self.int = int
        imgObject = Image("2.jpg")
        if int % 2 == 0:
            int += 1
        if self.mode == "g":
            ans = cv2.GaussianBlur(imgObject.img, (int, int), 0)
        elif self.mode == "m":
            ans = cv2.medianBlur(imgObject.img, int)
        elif self.mode == "b":
            ans = cv2.bilateralFilter(imgObject.img, int, 75, 75)
        cv2.imwrite("ui.jpg", ans)
        pixmap = QPixmap("ui.jpg")
        self.label.setPixmap(pixmap)


# crop window
class CropWindow(QMainWindow, my_form_crop):
    def __init__(self):
        super(CropWindow, self).__init__()
        self.setupUi(self)
        self.setWindowTitle("crop")
        self.ref_point = []
        self.pushButton_6.clicked.connect(self.next)
        self.pushButton_3.clicked.connect(self.prev)
        self.pushButton.clicked.connect(self.apply)
        self.imagename = "1"
        self.pushButton_4.clicked.connect(self.exit)
        self.setFixedSize(1269, 827)

        # remove title bar
        self.setWindowFlag(QtCore.Qt.FramelessWindowHint)
        self.setAttribute(QtCore.Qt.WA_TranslucentBackground)

    def prev(self):
        self.imagename = str(np.clip(int(self.imagename), 2, None) - 1)
        pixmap = QPixmap("./images/image" + self.imagename + ".jpg")
        pixmap = pixmap.scaled(600, 450)
        self.label.setPixmap(pixmap)
        if os.path.isfile("./cropped/croppedimage" + self.imagename + ".jpg"):
            pixmap = QPixmap("./cropped/croppedimage" + self.imagename + ".jpg")
        self.label_2.setPixmap(pixmap)

    def next(self):
        self.imagename = str(
            np.clip(int(self.imagename), None, UploadWindow._count - 1) + 1
        )
        pixmap = QPixmap("./images/image" + self.imagename + ".jpg")
        pixmap = pixmap.scaled(600, 450)
        self.label.setPixmap(pixmap)
        if os.path.isfile("./cropped/croppedimage" + self.imagename + ".jpg"):
            pixmap = QPixmap("./cropped/croppedimage" + self.imagename + ".jpg")
        self.label_2.setPixmap(pixmap)

    def apply(self):
        image = cv2.imread("ui.jpg")
        cv2.imwrite("./cropped/croppedimage" + self.imagename + ".jpg", image)

    def mousePressEvent(self, event):
        self.originQPoint = [event.x(), event.y()]
        self.ref_point.append(self.originQPoint)
        self.originQPoint = event.pos()
        self.currentQRubberBand = QtWidgets.QRubberBand(
            QtWidgets.QRubberBand.Rectangle, self
        )
        self.currentQRubberBand.setGeometry(
            QtCore.QRect(self.originQPoint, QtCore.QSize())
        )
        self.currentQRubberBand.show()

    def mouseMoveEvent(self, event):
        self.currentQRubberBand.setGeometry(
            QtCore.QRect(self.originQPoint, event.pos()).normalized()
        )

    def mouseReleaseEvent(self, event):
        self.endQPoint = [event.x(), event.y()]
        self.ref_point.append(self.endQPoint)
        self.currentQRubberBand.hide()
        currentQRect = self.currentQRubberBand.geometry()
        self.currentQRubberBand.deleteLater()
        if (
            self.ref_point[0][0] == self.ref_point[1][0]
            or self.ref_point[0][1] == self.ref_point[1][1]
        ):
            self.ref_point.clear()
            return
        imgObject = Image("./images/image" + self.imagename + ".jpg")
        image = cv2.resize(imgObject.img, (600, 450))
        if self.ref_point[0][1] < 280:
            self.ref_point[0][1] = 280
        if self.ref_point[1][1] < 280:
            self.ref_point[1][1] = 280
        if self.ref_point[1][1] > 730:
            self.ref_point[1][1] = 730
        if self.ref_point[0][1] > 730:
            self.ref_point[0][1] = 730
        if self.ref_point[0][0] < 30:
            self.ref_point[0][0] = 30
        if self.ref_point[1][0] < 30:
            self.ref_point[1][0] = 30
        if self.ref_point[0][0] > 630:
            self.ref_point[0][0] = 630
        if self.ref_point[1][0] > 630:
            self.ref_point[1][0] = 630
        croped = image[
            min(self.ref_point[0][1], self.ref_point[1][1])
            - 280 : max(self.ref_point[0][1], self.ref_point[1][1])
            - 280,
            min(self.ref_point[0][0], self.ref_point[1][0])
            - 30 : max(self.ref_point[0][0], self.ref_point[1][0])
            - 30,
        ]
        cv2.imwrite("ui.jpg", croped)
        pixmap = QPixmap("ui.jpg")
        self.label_2.setPixmap(pixmap)
        self.ref_point.clear()

    def exit(self):
        self.close()


# tag window
class TaggingWindow(QMainWindow, my_form_tag):
    def __init__(self):
        super(TaggingWindow, self).__init__()
        self.setupUi(self)
        self.setWindowTitle("Tagging")
        self.ref_point = [None, None]
        self.pushButton_4.clicked.connect(self.exit)
        self.pushButton_6.clicked.connect(self.next)
        self.pushButton_3.clicked.connect(self.prev)
        self.pushButton.clicked.connect(self.apply)
        self.imagename = "1"
        self.totalTexts = []
        self.lineEdit.hide()
        self.lineEdit.returnPressed.connect(self.tag)
        # remove title bar
        self.setWindowFlag(QtCore.Qt.FramelessWindowHint)
        self.setAttribute(QtCore.Qt.WA_TranslucentBackground)
        self.setFixedSize(1269, 827)

    def prev(self):
        self.imagename = str(np.clip(int(self.imagename), 2, None) - 1)
        pixmap = QPixmap("./images/image" + self.imagename + ".jpg")
        pixmap = pixmap.scaled(600, 450)
        self.label.setPixmap(pixmap)
        if os.path.isfile("./tagged/taggedimage" + self.imagename + ".jpg"):
            pixmap = QPixmap("./tagged/taggedimage" + self.imagename + ".jpg")
        elif os.path.isfile("./tagged/taggedimage" + self.imagename + ".jpg"):
            pixmap = QPixmap("./tagged/taggedimage" + self.imagename + ".jpg")

        pixmap = pixmap.scaled(600, 450)
        self.label_2.setPixmap(pixmap)
        self.lineEdit.hide()

    def next(self):
        self.lineEdit.hide()
        self.imagename = str(
            np.clip(int(self.imagename), None, UploadWindow._count - 1) + 1
        )
        pixmap = QPixmap("./images/image" + self.imagename + ".jpg")
        pixmap = pixmap.scaled(600, 450)
        self.label.setPixmap(pixmap)
        if os.path.isfile("./tagged/taggedimage" + self.imagename + ".jpg"):
            pixmap = QPixmap("./tagged/taggedimage" + self.imagename + ".jpg")
        pixmap = pixmap.scaled(600, 450)
        self.label_2.setPixmap(pixmap)

    def apply(self):
        image = cv2.imread("ui.jpg")
        cv2.imwrite("./tagged/taggedimage" + self.imagename + ".jpg", image)
        file1 = open("./tagged/ref_pointsOfimage" + self.imagename + ".txt", "a")
        file1.write(
            str((self.ref_point[0][0] - 30) * len(self.imgobj.img[0]) // 600)
            + ","
            + str((self.ref_point[0][1] - 280) * len(self.imgobj.img) // 450)
            + ","
            + str((self.ref_point[1][0] - 30) * len(self.imgobj.img[0]) // 600)
            + ","
            + str((self.ref_point[1][1] - 280) * len(self.imgobj.img) // 450)
            + "->"
            + self.totalTexts[-1]
            + "\n"
        )
        file1.close()

    def tag(self):
        self.totalTexts.append(self.lineEdit.text())
        imageObject = Image("ui.jpg")
        image = imageObject.img
        self.x += 1
        self.y += 15
        cv2.putText(
            image,
            self.totalTexts[-1],
            (self.x, self.y),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.5,
            (255, 0, 120),
            2,
        )
        cv2.imwrite("ui.jpg", image)
        pixmap = QPixmap("ui.jpg")
        self.label_2.setPixmap(pixmap)
        self.lineEdit.clear()
        self.lineEdit.hide()

    def mousePressEvent(self, event):
        self.originQPoint = [event.x(), event.y()]
        self.ref_point[0] = self.originQPoint
        self.originQPoint = event.pos()
        self.currentQRubberBand = QtWidgets.QRubberBand(
            QtWidgets.QRubberBand.Rectangle, self
        )
        self.currentQRubberBand.setGeometry(
            QtCore.QRect(self.originQPoint, QtCore.QSize())
        )
        self.currentQRubberBand.show()

    def mouseMoveEvent(self, event):
        self.currentQRubberBand.setGeometry(
            QtCore.QRect(self.originQPoint, event.pos()).normalized()
        )

    def mouseReleaseEvent(self, event):
        self.endQPoint = [event.x(), event.y()]
        self.ref_point[1] = self.endQPoint
        self.currentQRubberBand.hide()
        currentQRect = self.currentQRubberBand.geometry()
        self.currentQRubberBand.deleteLater()
        if (
            self.ref_point[0][0] == self.ref_point[1][0]
            or self.ref_point[0][1] == self.ref_point[1][1]
        ):
            return
        imgObject = Image("./images/image" + self.imagename + ".jpg")
        self.imgobj = imgObject
        if os.path.isfile("./tagged/taggedimage" + self.imagename + ".jpg"):
            imgObject = Image("./tagged/taggedimage" + self.imagename + ".jpg")
        image = cv2.resize(imgObject.img, (600, 450))
        pixmap = QPixmap("./images/image" + self.imagename + ".jpg")
        pixmap = pixmap.scaled(600, 450)
        self.label.setPixmap(pixmap)
        if self.ref_point[0][1] < 280:
            self.ref_point[0][1] = 280
        if self.ref_point[1][1] < 280:
            self.ref_point[1][1] = 280
        if self.ref_point[1][1] > 730:
            self.ref_point[1][1] = 730
        if self.ref_point[0][1] > 730:
            self.ref_point[0][1] = 730
        if self.ref_point[0][0] < 30:
            self.ref_point[0][0] = 30
        if self.ref_point[1][0] < 30:
            self.ref_point[1][0] = 30
        if self.ref_point[0][0] > 630:
            self.ref_point[0][0] = 630
        if self.ref_point[1][0] > 630:
            self.ref_point[1][0] = 630
        self.x = min(self.ref_point[0][0], self.ref_point[1][0]) - 30
        x2 = max(self.ref_point[0][0], self.ref_point[1][0]) - 30
        self.y = min(self.ref_point[0][1], self.ref_point[1][1]) - 280
        y2 = max(self.ref_point[0][1], self.ref_point[1][1]) - 280

        image = cv2.rectangle(
            image,
            (self.x, self.y),
            (x2, y2),
            (255, 0, 255),
            1,
        )
        self.lineEdit.show()
        cv2.imwrite("ui.jpg", image)
        pixmap = QPixmap("ui.jpg")
        self.label_2.setPixmap(pixmap)

    def exit(self):
        self.close()


# filtering
class FilteringWindow(QMainWindow, my_form_filtering):
    def __init__(self):
        super(FilteringWindow, self).__init__()
        self.setupUi(self)
        self.setWindowTitle("filtering")

        # remove title bar
        self.setWindowFlag(QtCore.Qt.FramelessWindowHint)
        self.setAttribute(QtCore.Qt.WA_TranslucentBackground)

        self.pushButton.clicked.connect(self.apply_invert)
        self.pushButton_2.clicked.connect(self.apply_sepia)
        self.pushButton_3.clicked.connect(self.destroy)
        self.pushButton_4.clicked.connect(self.Morphological)
        self.pushButton_5.clicked.connect(self.openning)
        self.pushButton_6.clicked.connect(self.grayScale)
        self.pushButton_7.clicked.connect(self.denoise)
        self.pushButton_8.clicked.connect(self.exit)
        self.pushButton_9.clicked.connect(self.applyToAll)
        self.setFixedSize(1249, 801)

    def exit(self):
        self.close()

    def applyToAll(self):
        my_list = allImagesInThisDirectory("./images")
        t = 0
        for img in my_list:
            t += 1
            if self.mode == "i":
                ans = cv2.bitwise_not(img)
            elif self.mode == "g":
                ans = img.grayScale()
            elif self.mode == "s":
                ans = img.apply_sepia()
            elif self.mode == "d":
                ans = img.destroy()
            elif self.mode == "m":
                ans = img.Morphological()
            elif self.mode == "o":
                ans = img.openning()
            elif self.mode == "n":
                ans = img.denoise()
            UploadWindow._count += 1
            cv2.imwrite(".\images\image" + str(UploadWindow._count) + ".jpg", ans)
            cv2.imwrite(".\images\image" + str(UploadWindow._count) + ".jpg", ans)
            if os.path.isfile("./tagged/ref_pointsOfimage" + str(t) + ".txt"):
                file1 = open("./tagged/ref_pointsOfimage" + str(t) + ".txt", "r")
                lines = file1.read().split("\n")
                file1.close()
                for line in lines:
                    if line == "":
                        continue
                    points, text = line.split("->")
                    x0, y0, xp0, yp0 = points.split(",")
                    x0, y0, xp0, yp0 = int(x0), int(y0), int(xp0), int(yp0)
                    xmin = min(x0, xp0)
                    ymin = min(y0, yp0)
                    xmax = max(x0, xp0)
                    ymax = max(y0, yp0)
                    file1 = open(
                        "./tagged/ref_pointsOfimage"
                        + str(UploadWindow._count)
                        + ".txt",
                        "a",
                    )
                    file1.write(
                        str(xmin)
                        + ","
                        + str(ymin)
                        + ","
                        + str(xmax)
                        + ","
                        + str(ymax)
                        + "->"
                        + text
                        + "\n"
                    )
                    file1.close()

    def apply_invert(self):
        self.mode = "i"
        imgObject = cv2.imread("2.jpg")
        cv2.imwrite("ui.jpg", cv2.bitwise_not(imgObject))
        pixmap = QPixmap("ui.jpg")
        self.label_filtering.setPixmap(pixmap)

    def grayScale(self):
        self.mode = "g"
        imgObject = cv2.imread("2.jpg")
        gray = imgObject.copy()
        gray = gray.astype(np.float)
        gray[:, :, 0] = gray[:, :, 1] = gray[:, :, 2] = 1.5 * np.mean(imgObject, 2)
        gray[gray > 255] = 255
        gray = gray.astype(np.uint8)
        cv2.imwrite("ui.jpg", (gray))
        pixmap = QPixmap("ui.jpg")
        self.label_filtering.setPixmap(pixmap)

    def apply_sepia(self):
        self.mode = "s"
        img = cv2.imread("2.jpg")
        img = np.array(img, dtype=np.float64)  # converting to float to prevent loss
        img = cv2.transform(
            img,
            np.matrix(
                [[0.393, 0.769, 0.189], [0.349, 0.686, 0.168], [0.272, 0.534, 0.869]]
            ),
        )  # multipying image with special sepia matrix
        img[np.where(img > 255)] = 255  # normalizing values greater than 255 to 255
        img = np.array(img, dtype=np.uint8)  # converting back to int
        cv2.imwrite("ui.jpg", cv2.bitwise_not(img))
        pixmap = QPixmap("ui.jpg")
        self.label_filtering.setPixmap(pixmap)

    def destroy(self):
        self.mode = "d"
        img = cv2.imread("2.jpg")
        hsv = cv2.cvtColor(img, cv2.COLOR_RGB2HSV)
        lower_red = np.array([10, 10, 10])
        upper_red = np.array([240, 240, 240])
        mask = cv2.inRange(hsv, lower_red, upper_red)
        res = cv2.bitwise_and(img, img, mask=mask)
        cv2.imwrite("ui.jpg", res)
        pixmap = QPixmap("ui.jpg")
        self.label_filtering.setPixmap(pixmap)

    def Morphological(self):
        self.mode = "m"
        img = cv2.imread("2.jpg", 0)
        kernel = np.ones((5, 5), np.uint8)
        gradient = cv2.morphologyEx(img, cv2.MORPH_GRADIENT, kernel)
        cv2.imwrite("ui.jpg", gradient)
        pixmap = QPixmap("ui.jpg")
        self.label_filtering.setPixmap(pixmap)

    def openning(self):
        self.mose = "o"
        img = cv2.imread("2.jpg", 0)
        kernel = np.ones((5, 5), np.uint8)
        openning = cv2.morphologyEx(img, cv2.MORPH_OPEN, kernel)
        cv2.imwrite("ui.jpg", openning)
        pixmap = QPixmap("ui.jpg")
        self.label_filtering.setPixmap(pixmap)

    def denoise(self):
        self.mode = "n"
        imgObject = Image("2.jpg")
        img = imgObject.denoise()
        cv2.imwrite("ui.jpg", img)
        pixmap = QPixmap("ui.jpg")
        self.label_filtering.setPixmap(pixmap)


# Split
class SplitWindow(QMainWindow, my_form_split):
    def __init__(self):
        super(SplitWindow, self).__init__()
        self.setupUi(self)
        self.setWindowTitle("Split")

        # remove title bar
        self.setWindowFlag(QtCore.Qt.FramelessWindowHint)
        self.setAttribute(QtCore.Qt.WA_TranslucentBackground)
        self.setFixedSize(891, 431)

        imagePath = ".\images"
        list_of_images_directory = allImagesInThisDirectory2(imagePath)
        self.num = len(list_of_images_directory)
        if self.num == 0:
            self.label_3.setText("You did not upload images!")
        self.label.setText(f"{self.num}")
        self.ch = 0
        self.Enter.clicked.connect(self.enter_pressed)
        self.OK_Button.clicked.connect(self.OK_pressed)
        self.pushButton_4.clicked.connect(self.exit)

    def exit(self):
        self.close()

    def enter_pressed(self):
        if self.lineEdit.text() != "":
            self.ch = 1
            pTrain = float(self.lineEdit.text())
            if pTrain > 100 or pTrain < 0:
                self.label_3.setText("it is not percentage!")
            else:
                self.label_3.clear()
                self.train = int(pTrain * self.num / 100)
                self.label_4.setText(
                    f"The Split data number is :     {self.train} images for Train\n\t\t\t {self.num - self.train} images for Test\n\t\t\t  is it OK ?"
                )

    def OK_pressed(self):
        if self.ch == 0:
            self.label_3.setText("First Press Enter!")
        else:
            self.Trainlist = random.sample(range(1, self.num), self.train)
            self.doSplit()
            self.close()

    def doSplit(self):
        list_of_images_directory = allImagesInThisDirectory2(".\images")
        j = k = 1
        for i in range(len(list_of_images_directory)):
            pixmap = QPixmap(list_of_images_directory[i])
            if i in self.Trainlist:
                pixmap.save(f".\splitData\Train\image{j}.jpg")
                j += 1
            else:
                pixmap.save(f".\splitData\Test\image{k}.jpg")
                k += 1


# fast augmentation
class FastAugmentationWindow(QMainWindow, my_form_fast):
    def __init__(self):
        super(FastAugmentationWindow, self).__init__()
        self.setupUi(self)
        self.setWindowTitle("fast mode")
        self.setFixedSize(666, 828)

        # remove title bar
        self.setWindowFlag(QtCore.Qt.FramelessWindowHint)
        self.setAttribute(QtCore.Qt.WA_TranslucentBackground)

        self.comboBox.addItems(["None", "gaussian", "speckle", "salt", "pepper", "s&p"])
        self.comboBox_2.addItems(["None", "gaussian", "median", "bilateral"])
        self.pushButton_8.clicked.connect(self.applyToAll)
        self.pushButton_7.clicked.connect(self.exit)

    def applyToAll(self):
        my_file = allImagesInThisDirectory("./images")
        if self.lineEdit_8.text() != "":
            for i in range(int(self.lineEdit_8.text())):
                for image in my_file:
                    if self.lineEdit.text() != "" and self.lineEdit_2.text() != "":
                        image.img = cv2.resize(
                            image.img,
                            (
                                np.int(self.lineEdit.text()),
                                np.int(self.lineEdit_2.text()),
                            ),
                        )
                    if self.lineEdit_6.text() != "" and self.lineEdit_7.text() != "":
                        image.adjustBrightness(
                            1
                            + (
                                np.random.randint(
                                    int(self.lineEdit_7.text()),
                                    int(self.lineEdit_6.text()),
                                )
                                / 100
                            ),
                            True,
                        )
                    if self.lineEdit_3.text() != "" and self.lineEdit_4.text() != "":
                        image.rotate(
                            np.random.randint(
                                int(self.lineEdit_3.text()), int(self.lineEdit_4.text())
                            ),
                            True,
                        )
                    if (
                        self.checkBox.isChecked() == True
                        and self.checkBox_2.isChecked() == True
                    ):
                        x = np.random.randint(-1, 3)
                    elif self.checkBox.isChecked() == True:
                        x = int(str(np.random.randint(1, 3)) + "2") % 4
                    elif self.checkBox_2.isChecked() == True:
                        x = np.random.randint(1, 3)
                    else:
                        x = 2
                    if x != 2:
                        image.img = cv2.flip(image.img, x)
                    image.addnoise(
                        self.comboBox.currentText(),
                        np.random.randint(0, 20) / 100,
                        True,
                    )
                    rd = np.random.randint(10)
                    if rd % 2 == 0:
                        rd += 1
                    if self.comboBox_2.currentText() == "gaussian":
                        image.img = cv2.GaussianBlur(image.img, (rd, rd), 0)
                    elif self.comboBox_2.currentText() == "median":
                        image.img = cv2.medianBlur(image.img, rd)
                    elif self.comboBox_2.currentText() == "bilateral":
                        image.img = cv2.bilateralFilter(image.img, rd, 75, 75)
                    if self.checkBox_5.isChecked():
                        image.denoise(True)
                    UploadWindow._count += 1
                    if self.lineEdit_5.text() != "":
                        for crop in range(int(self.lineEdit_17.text())):
                            deltax = (
                                int(self.lineEdit_5.text()) * len(image.img[0]) // 100
                            )
                            deltay = int(self.lineEdit_5.text()) * len(image.img) // 100
                            x0 = np.random.randint(0, len(image.img[0]) - deltax + 1)
                            y0 = np.random.randint(0, len(image.img) - deltay + 1)
                            temp = image.crop(
                                (y0, y0 + deltay - 1), (x0, x0 + deltax - 1)
                            )
                            cv2.imwrite(
                                ".\images\Croppedimage"
                                + str(UploadWindow._count)
                                + "_"
                                + str(crop)
                                + ".jpg",
                                temp,
                            )

                    cv2.imwrite(
                        ".\images\image" + str(UploadWindow._count) + ".jpg", image.img
                    )

    def exit(self):
        self.close()


##making treeview pretty
class StandardItem(QStandardItem, my_form_main):
    def __init__(self, txt="", font_size=12, set_bold=False, color=QColor(0, 0, 0)):
        super().__init__()
        fnt = QFont("Open Sans", font_size)
        fnt.setBold(set_bold)
        self.setEditable(False)
        self.setForeground(color)
        # self.setBackground(color_b)
        self.setFont(fnt)
        self.setText(txt)


## application
class MainWindow(QMainWindow, my_form_main):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.setupUi(self)
        ##remove title bar
        self.setWindowFlag(QtCore.Qt.FramelessWindowHint)
        self.setAttribute(QtCore.Qt.WA_TranslucentBackground)
        self.resize(700, 500)
        self.setFixedSize(800, 529)

        ##tree
        treeView = QTreeView()
        treeView.setHeaderHidden(True)
        treeView.setAnimated(True)
        treeView.setIndentation(100)
        # treeView.setGeometry(QRect(0, 0, 882, 346))
        treeView.setStyleSheet(
            (
                "QTreeView {    \n"
                "    background-color: rgb(39, 44, 54);\n"
                "    padding: 10px;\n"
                "    border-radius: 15px;\n"
                "    gridline-color: rgb(44, 49, 60);\n"
                "    border-bottom: 1px solid rgb(44, 49, 60);\n"
                "}\n"
                "QTreeView::item{\n"
                "    border-color: rgb(44, 49, 60);\n"
                "    padding-left: 5px;\n"
                "    padding-right: 5px;\n"
                "    gridline-color: rgb(44, 49, 60);\n"
                "}\n"
                "QTreeView::item:selected{\n"
                "    background-color: rgb(85, 170, 255);\n"
                "}\n"
                "QScrollBar:horizontal {\n"
                "    border: none;\n"
                "    background: rgb(52, 59, 72);\n"
                "    height: 14px;\n"
                "    margin: 0px 21px 0 21px;\n"
                "    border-radius: 0px;\n"
                "}\n"
                " QScrollBar:vertical {\n"
                "    border: none;\n"
                "    background: rgb(52, 59, 72);\n"
                "    width: 14px;\n"
                "    margin: 21px 0 21px 0;\n"
                "    border-radius: 0px;\n"
                " }\n"
                "QHeaderView::section{\n"
                "    Background-color: rgb(39, 44, 54);\n"
                "    max-width: 30px;\n"
                "    border: 1px solid rgb(44, 49, 60);\n"
                "    border-style: none;\n"
                "    border-bottom: 1px solid rgb(44, 49, 60);\n"
                "    border-right: 1px solid rgb(44, 49, 60);\n"
                "}\n"
                "QTreeView::horizontalHeader {    \n"
                "    background-color: rgb(81, 255, 0);\n"
                "}\n"
                "QHeaderView::section:horizontal\n"
                "{\n"
                "    border: 1px solid rgb(32, 34, 42);\n"
                "    background-color: rgb(27, 29, 35);\n"
                "    padding: 3px;\n"
                "    border-top-left-radius: 20px;\n"
                "    border-top-right-radius: 20px;\n"
                "}\n"
                "QHeaderView::section:vertical\n"
                "{\n"
                "    border: 1px solid rgb(44, 49, 60);\n"
                "}\n"
                "QTreeView QTreeViewCornerButton::section\n"
                "{\n"
                "background-color:red\n"
                "}\n"
                ""
            )
        )
        treeModel = QStandardItemModel()
        rootNode = treeModel.invisibleRootItem()
        #########################################################
        source_images = StandardItem(
            "Source Images", 35, color=QColor(96, 100, 152), set_bold=True
        )
        upload = StandardItem("Upload", 25, color=QColor(254, 121, 199))
        source_images.appendRow(upload)

        annotate = StandardItem(
            "Annotate", 35, color=QColor(96, 100, 152), set_bold=True
        )
        tagging = StandardItem("Tagging", 25, color=QColor(254, 121, 199))
        annotate.appendRow(tagging)

        preprocessing = StandardItem(
            "Preprocessing", 35, color=QColor(96, 100, 152), set_bold=True
        )
        resize = StandardItem("Resize", 25, color=QColor(254, 121, 199))
        preprocessing.appendRow(resize)

        augmentation = StandardItem(
            "Augmentation", 35, color=QColor(96, 100, 152), set_bold=True
        )
        flip = StandardItem("Flip", 25, color=QColor(254, 121, 199))
        crop = StandardItem("Crop", 25, color=QColor(254, 121, 199))
        rotation = StandardItem("Rotation", 25, color=QColor(254, 121, 199))
        brightness = StandardItem("Brightness", 25, color=QColor(254, 121, 199))
        noise = StandardItem("Noise", 25, color=QColor(254, 121, 199))
        blurring = StandardItem("Blurring", 25, color=QColor(254, 121, 199))
        filtering = StandardItem("Filtering", 25, color=QColor(254, 121, 199))
        augmentation.appendRow(flip)
        augmentation.appendRow(crop)
        augmentation.appendRow(rotation)
        augmentation.appendRow(brightness)
        augmentation.appendRow(noise)
        augmentation.appendRow(blurring)
        augmentation.appendRow(filtering)

        tran_test_split = StandardItem(
            "Train/Test Split", 35, color=QColor(96, 100, 152), set_bold=True
        )
        split = StandardItem("Split", 25, color=QColor(254, 121, 199))
        tran_test_split.appendRow(split)

        fast = StandardItem("Fast Mode", 35, color=QColor(96, 100, 152), set_bold=True)
        fastAugmentation = StandardItem(
            "Fast Augmentation", 25, color=QColor(254, 121, 199)
        )
        fast.appendRow(fastAugmentation)

        rootNode.appendRow(source_images)
        rootNode.appendRow(annotate)
        rootNode.appendRow(preprocessing)
        rootNode.appendRow(augmentation)
        rootNode.appendRow(tran_test_split)
        rootNode.appendRow(fast)

        treeView.setModel(treeModel)
        treeView.expandAll()

        treeView.doubleClicked.connect(self.action)

        self.setCentralWidget(treeView)

    def action(self, val):
        if val.data() == "Upload":
            self.flip = UploadWindow()
            self.flip.show()
        if val.data() == "Flip":
            self.flip = FlipWindow()
            self.flip.show()
        if val.data() == "Resize":
            self.flip = ResizeWindow()
            self.flip.show()
        if val.data() == "Brightness":
            self.brightness = BrightnessWindow()
            self.brightness.show()
        if val.data() == "Rotation":
            self.rotation = RotationWindow()
            self.rotation.show()
        if val.data() == "Noise":
            self.noise = NoiseWindow()
            self.noise.show()
        if val.data() == "Blurring":
            self.blurring = BlurringWindow()
            self.blurring.show()
        if val.data() == "Crop":
            self.crop = CropWindow()
            self.crop.show()
        if val.data() == "Tagging":
            self.tag = TaggingWindow()
            self.tag.show()
        if val.data() == "Filtering":
            self.filtering = FilteringWindow()
            self.filtering.show()
        if val.data() == "Split":
            self.split = SplitWindow()
            self.split.show()
        if val.data() == "Fast Augmentation":
            self.fastAugmentation = FastAugmentationWindow()
            self.fastAugmentation.show()


## splash screen
class SplashScreen(QMainWindow, my_form_SplashScreen):
    def __init__(self):
        super(SplashScreen, self).__init__()
        self.setupUi(self)
        ##remove title bar
        self.setWindowFlag(QtCore.Qt.FramelessWindowHint)
        self.setAttribute(QtCore.Qt.WA_TranslucentBackground)
        ##drop shadow effect
        self.shadow = QGraphicsDropShadowEffect(self)
        self.shadow.setBlurRadius(20)
        self.shadow.setXOffset(0)
        self.shadow.setYOffset(0)
        self.shadow.setColor(QColor(0, 0, 0, 60))
        self.dropShadowFrame.setGraphicsEffect(self.shadow)
        ##Qtimer ==> start
        self.timer = QtCore.QTimer()
        self.timer.timeout.connect(self.progress)
        ##timer in ms
        self.timer.start(10)
        # change description
        self.label_description.setText("<strong>WELCOME</strong> TO OUR APPLICATION")
        QtCore.QTimer.singleShot(
            500,
            lambda: self.label_description.setText(" PREPROCESSING AND AUGMENTATION "),
        )

    def progress(self):
        global Counter
        # set value to progress bar
        self.progressBar.setValue(Counter)
        # close splash screen and open app
        if Counter > 100:
            # stop timer
            self.timer.stop()
            # show main window
            self.main = MainWindow()
            self.main.show()
            # close splash screen
            self.close()
        # increase counter
        Counter += 1


folders = [
    "./images",
    "./cropped",
    "./tagged",
    "./splitData",
    "./splitData/Test",
    "./splitData/Train",
]
for f in folders:
    if os.path.isdir(f):
        shutil.rmtree(f)
    os.mkdir(f)


app = QApplication([])
w = SplashScreen()
w.show()
sys.exit(app.exec_())
