import numpy as np
import cv2
from skimage.util import random_noise


class Image:
    def __init__(self, input=None):
        if type(input) == type(str()):
            self.img = cv2.imread(input)
        elif type(input) == type(list()):
            self.img = input
        else:
            self.img = None

    def adjustBrightness(self, br, save=False):
        temp = self.img.astype(np.int)
        temp = temp * br
        temp[temp > 255] = 255
        temp = temp.astype(np.uint8)
        if save > 0:
            self.img = temp
        return temp

    def edge(self, save=False):
        temp = cv2.Canny(self.img, 100, 200)
        if save == True:
            self.img = temp
        return temp

    def edgePriserving(self, save=False):
        temp = cv2.edgePreservingFilter(self.img)
        if save == True:
            self.img = temp
        return temp

    def contoured(self, save=False):
        edged = self.edge()
        # Finding Contours
        contour, hier = cv2.findContours(
            edged, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE
        )
        # print("Count of Contours  = " + str(len(contour)))
        if save == False:
            temp = self.img.copy()
        return cv2.drawContours(temp, contour, -1, (0, 0, 255), 1)

    def crop(self, height, width, save=False):
        temp = self.img[height[0] : height[1], width[0] : width[1], :]
        if save == True:
            self.img = temp
        return temp

    #       'gauss'     Gaussian-distributed additive noise.
    #       'poisson'   Poisson-distributed noise generated from the data.
    #       's&p'       Replaces random pixels with 0 or 1.
    #       'speckle'   Multiplicative noise using out = image + n*image,where
    #                   n is uniform noise with specified mean & variance.
    #       x = var :
    #       Variance of random distribution. Used in ‘gaussian’ and ‘speckle’.
    #       x = amount :
    #       Proportion of image pixels to replace with noise on range [0, 1]. Used in ‘salt’, ‘pepper’, and ‘salt & pepper’.

    def addnoise(self, mode, x=0.05, save=False):
        if mode == "gaussian" or mode == "speckle":
            gimg = random_noise(self.img, mode=mode, var=x * 2)
        elif mode == "s&p" or mode == "pepper" or mode == "salt":
            gimg = random_noise(self.img, mode=mode, amount=x)
        elif mode == "poisson":
            gimg = random_noise(self.img, mode=mode)
        else:
            return self.img
        gimg = np.floor(gimg * 255).astype(np.uint8)
        if save == True:
            self.img = gimg
        return gimg

    def rotate(self, angle, save=False):
        rows, cols, bgr = self.img.shape
        # cols-1 and rows-1 are the coordinate limits.
        M = cv2.getRotationMatrix2D(((cols - 1) / 2.0, (rows - 1) / 2.0), angle, 1)
        dst = cv2.warpAffine(self.img, M, (cols, rows))
        if save == True:
            self.img = dst
        return dst

    def denoise(self, save=False):
        temp = cv2.fastNlMeansDenoisingColored(self.img, None, 10, 10, 7, 15)
        if save == True:
            self.img = temp
        return temp

    def grayScale(self):
        gray = self.img.copy()
        gray = gray.astype(np.float)
        gray[:, :, 0] = gray[:, :, 1] = gray[:, :, 2] = 1.5 * np.mean(gray, 2)
        gray[gray > 255] = 255
        gray = gray.astype(np.uint8)
        return gray

    def apply_sepia(self):
        sepia = np.array(
            self.img, dtype=np.float64
        )  # converting to float to prevent loss
        sepia = cv2.transform(
            sepia,
            np.matrix(
                [[0.393, 0.769, 0.189], [0.349, 0.686, 0.168], [0.272, 0.534, 0.869]]
            ),
        )  # multipying image with special sepia matrix
        sepia[np.where(sepia > 255)] = 255  # normalizing values greater than 255 to 255
        sepia = np.array(sepia, dtype=np.uint8)  # converting back to int
        return sepia

    def destroy(self):
        hsv = cv2.cvtColor(self.img, cv2.COLOR_RGB2HSV)
        lower_red = np.array([10, 10, 10])
        upper_red = np.array([240, 240, 240])
        mask = cv2.inRange(hsv, lower_red, upper_red)
        res = cv2.bitwise_and(self.img, self.img, mask=mask)
        return res

    def Morphological(self):
        kernel = np.ones((5, 5), np.uint8)
        gradient = cv2.morphologyEx(self.img, cv2.MORPH_GRADIENT, kernel)
        return gradient

    def openning(self):
        kernel = np.ones((5, 5), np.uint8)
        openning = cv2.morphologyEx(self.img, cv2.MORPH_OPEN, kernel)
        return openning
