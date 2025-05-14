import numpy as np
import  cv2

img = cv2.imread('data/lesson1/Lenna.png',
                 cv2.IMREAD_GRAYSCALE
                 )

cv2.imshow("image",
           img)

mask = img >128
print(img[mask])
img[mask] =255
img[~mask] =0
cv2.imshow("image",
           img)

cv2.waitKey(0)

img1 = cv2.imread('data/lesson1/baboo.jpg',
                 cv2.IMREAD_GRAYSCALE
                 )

print(img1.shape)
img1[:20, :] = 0
img1[-210:,: ] = 0
img1[:, -60:] = 0
img1[:,: 60] = 0

cv2.imshow("image1",
           img1)

cv2.waitKey(0)
