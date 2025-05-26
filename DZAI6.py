# Для наступних зображень зображень:
#  data/lesson4/apple.png
#  data/lesson4/apple_noised.png
#  data/lesson4/apple_salt_pepper.png
# використовуючи гаусове розмиття, виявлення країв та
# морфологічні оператори, отримайте краї яблука.
import cv2
import numpy as np
import utils


img = cv2.imread("data/lesson4/apple.png", cv2.IMREAD_GRAYSCALE)
img1 = cv2.imread("data/lesson4/apple_noised.png", cv2.IMREAD_GRAYSCALE)
img2 = cv2.imread("data/lesson4/apple_salt_pepper.png", cv2.IMREAD_GRAYSCALE)


@utils.trackbar_decorator(lower=(0, 255), upper=(0, 255))
def func(gray, lower, upper):
    gray = cv2.GaussianBlur(gray,
                            (21, 21),
                            sigmaX=2.5)

    # алгоритм Canny(пошук меж)7214711
    edged = cv2.Canny(gray, lower, upper)

    return edged

#func(img)
#func(img1)
#func(img2)
#
img = cv2.GaussianBlur(img, (7,7), 2 )
eng = cv2.Canny(img, 80, 175)
kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (3,3))
dilate = cv2.dilate(eng, kernel, iterations=4)
erode = cv2.erode(dilate, kernel, iterations=4)

cv2.imshow("original", img)
cv2.imshow("eng", eng)
cv2.imshow("dilate", dilate)
cv2.imshow("erode", erode)
cv2.waitKey(0)

img1 = cv2.GaussianBlur(img1, (11,11), 2 )
eng1 = cv2.Canny(img1, 91, 124)
kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (3,3))
dilate1 = cv2.dilate(eng1, kernel, iterations=6)
erode1 = cv2.erode(dilate1, kernel, iterations=4)

cv2.imshow("original", img1)
cv2.imshow("eng", eng1)
cv2.imshow("dilate", dilate1)
cv2.imshow("erode", erode1)
cv2.waitKey(0)

img2 = cv2.GaussianBlur(img2, (21,21), 2.5 )
eng2 = cv2.Canny(img2, 59, 118)
kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (3,3))
dilate2 = cv2.dilate(eng2, kernel, iterations=13)
erode2 = cv2.erode(dilate2, kernel, iterations=9)

cv2.imshow("original", img2)
cv2.imshow("eng", eng2)
cv2.imshow("dilate", dilate2)
cv2.imshow("erode", erode2)
cv2.waitKey(0)