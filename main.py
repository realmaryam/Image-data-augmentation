import cv2
from image import Image
from funcs import allImagesInThisDirectory, eazyCrop, label

# test      of       allImagesInThisDirectory()
list_of_all_images = allImagesInThisDirectory(".")
for i in range(len(list_of_all_images)):
    list_of_all_images[i].img = cv2.resize(list_of_all_images[i].img, (480, 320))
    cv2.imshow(str(i), list_of_all_images[i].img)
cv2.waitKey()
cv2.destroyAllWindows()


# test      of       Image methodes
imgObject = Image("test.jpeg")
imgObject.img = cv2.resize(imgObject.img, (800, 600))
img1 = imgObject.img
img2 = cv2.cvtColor(imgObject.img, cv2.COLOR_BGR2LAB)
img3 = imgObject.adjustBrightness(1.5)
img4 = imgObject.edge()
img5 = imgObject.edgePriserving()
img6 = imgObject.contoured()

# cv2.ROTATE_90_CLOCKWISE & cv2.ROTATE_90_COUNTERCLOCKWISE are possible
img7 = cv2.rotate(imgObject.img, cv2.ROTATE_90_CLOCKWISE)

# 0 means flipping around the x-axis and positive value (for example, 1) means flipping around y-axis.
# Negative value (for example, -1) means flipping around both axes.
img8 = cv2.flip(imgObject.img, 0)
img9 = imgObject.crop([0, 399], [140, 500])

img10 = imgObject.rotate(30)
img11 = imgObject.addnoise("s&p", 0.5, save=True)
img12 = imgObject.denoise()


# Gaussian Blur
Gaussian = cv2.GaussianBlur(img1, (9, 9), 0)
# Median Blur
median = cv2.medianBlur(img11, 9)
# Bilateral Blur
bilateral = cv2.bilateralFilter(img1, 15, 75, 75)


# For img1-img12
cv2.imshow("original", img1)
cv2.imshow("noisy", img11)
cv2.imshow("denoised", img12)
cv2.waitKey()
cv2.destroyAllWindows()


# test      of       eazyCrop()
# select a rectangle then press 'c' to crop or 'r' to reset the photo
croped = eazyCrop(img1)
cv2.imshow("croped", croped)
cv2.waitKey()
cv2.destroyAllWindows()

# test      of       label()
# select a rectangle, press 'l' and then enter your text to label
labeled = label(img1)
cv2.imshow("labeled", labeled[0])
cv2.waitKey()
cv2.destroyAllWindows()
