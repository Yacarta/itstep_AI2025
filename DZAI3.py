import  cv2
import utils
# Відкрийте зображення data/lesson2/darken.png
# Переведіть його в формат HSV
# Далі для каналу value зробіть одну з двох обробок
# 1. Застосуйте вирівнювання гістограм
img = cv2.imread("data/lesson2/darken.png ")
hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
hsv[:,:, 0] = cv2.equalizeHist(hsv[:,:, 0])
new_img = cv2.cvtColor(hsv, cv2.COLOR_HSV2BGR)
cv2.imshow("original", img)
cv2.imshow("hsv", hsv)
cv2.waitKey(0)
# 2. Збільшіть значення десь на 20-50%, для цього
# o Помножте усі значення value на відповідне
# число
# o Оскільки ви вийдете за межі діапазону 0-255
# застосуйте
# np.clip(value, 0, 255)
# o  Оскільки результат не ціле число
# value.astype(np.unit8)
# o Напишіть для цієї частини функцію з
# utils.trackbar_decorator
# Переведіть результат назад у формат BGR
# Виведіть результат для двох варіантів обробоки
import utils
import numpy as np
# @utils.trackbar_decorator

def increase_value(intensity=30):
    h, s, v = cv2.split(hsv.copy())
    factor = 1 + (intensity / 100.0)
    v_new = np.clip(v * factor, 0, 255).astype(np.uint8)
    hsv_new = cv2.merge([h, s, v_new])

    return hsv_new


new = increase_value()
result_bright = cv2.cvtColor(new, cv2.COLOR_HSV2BGR)
cv2.imshow("hsv1", result_bright)
cv2.waitKey(0)

new1 = increase_value(20)
result_bright = cv2.cvtColor(new1, cv2.COLOR_HSV2BGR)
cv2.imshow("hsv2", result_bright)
cv2.waitKey(0)

new2 = increase_value(80)
result_bright = cv2.cvtColor(new2, cv2.COLOR_HSV2BGR)
cv2.imshow("hsv3", result_bright)
cv2.waitKey(0)



