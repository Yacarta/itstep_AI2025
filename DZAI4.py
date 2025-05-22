import cv2
# Завдання 1
# Відкрийте зображення data/lesson3/sonet.png. Проведіть
# бінарізацію.
# Обов’язково використайте:
#  розмиття або наведення різкості
#  адаптивну бінарізацію
#  очищеня шумів

img = cv2.imread("data/lesson3/sonet.png")
cv2.imshow("orig", img)
# бінарізація(звичайна)
img_gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
threshold = 128
result = img_gray.copy()

mask = img_gray > threshold

result[mask] = 255
result[~mask] = 0
cv2.imshow("gray", img_gray)
cv2.imshow("bin", result)
cv2.waitKey(0)
#  розмиття або наведення різкості
new_sharp = cv2.GaussianBlur(img_gray,  # оригільне зображення
                           ksize=(3, 3), # розмір ядра\фільра\рамки
                           sigmaX=100  # чим більше тим сильніше розмиття
                           )
cv2.imshow("sharp", new_sharp)
cv2.waitKey(0)
#  очищеня шумів
new_img = cv2.bilateralFilter(img_gray,  # оригільне зображення
                              d=5,  # розмір ядра\фільра\рамки
                              sigmaColor=75,  # впливає на коефіцієнт за кольором
                              sigmaSpace=75,  # вплива на коефіцієнти як в гауса
                              )
#  адаптивну бінарізацію
result2 = cv2.adaptiveThreshold(new_img,  # оригільне зображення(чорнобіле)
                                255, # інтенсивність пікселів білого кольору
                                cv2.ADAPTIVE_THRESH_GAUSSIAN_C,  # алгоритм як рахувати threshold
                                cv2.THRESH_BINARY,  # тип бінарізації
                                11,  # розмір ядра\фільра\рамки
                                2,  # наскільки сильною є бінарізацію
                                )
cv2.imshow("binadap", result2)
cv2.waitKey(0)

# Завдання 2
# Відкрийте зображення data/lesson3/sonnet_noised.png.
# Проведіть бінарізацію. Застосуйте код з завдання 1 та
# спробуйте покращити результат

img1 = cv2.imread("data/lesson3/sonet_noised.png")


img_gray1 = cv2.cvtColor(img1, cv2.COLOR_BGR2GRAY)
threshold = 110
result = img_gray1.copy()

mask = img_gray1 > threshold

result[mask] = 255
result[~mask] = 0

#  розмиття або наведення різкості
new_sharp = cv2.GaussianBlur(img_gray1,
                           ksize=(3, 3),
                           sigmaX=100
                           )

#  очищеня шумів
new_img = cv2.bilateralFilter(img_gray1,
                              d=5,
                              sigmaColor=50,
                              sigmaSpace=50,
                              )
#  адаптивну бінарізацію
result3 = cv2.adaptiveThreshold(new_img,
                                255,
                                cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
                                cv2.THRESH_BINARY,
                                11,
                                0.5,
                                )
cv2.imshow("binadap", result3)
cv2.imshow("shum", new_img)
cv2.imshow("sharp", new_sharp)
cv2.imshow("orig", img1)
cv2.imshow("gray", img_gray1)
cv2.imshow("bin", result)
cv2.waitKey(0)
