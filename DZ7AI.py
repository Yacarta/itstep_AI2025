# Відкрийте зображення data/lesson_seg/tumor1.jpg
# Проведіть сегментацію зображення використовуючи
# модель data/lesson_seg/brain-tumor-seg.jpg
# Визначте площу пухлини в пікселях.
# Визначте площу в
# (1 піксель – 0,0025
# )
# В залежності від площі присвойте пухлині певний тип
#  <10     – small
#  10-25     – middle
#  >25    – large
# Покажіть пухлину – за допомогою маски усі лишні
# пікселі зробіть 0, а як назву зображення використайте її тип

import cv2
import ultralytics
import numpy as np

img = cv2.imread("data/lesson_seg/lesson_seg/tumor1.jpg")
model = ultralytics.YOLO('data/lesson_seg/lesson_seg/brain-tumor-seg.pt')

results = model.predict(img)

result = results[0]


print(result.boxes)

masks = result.masks.data.numpy()

result.show()
masks = result.masks.data

# перевести в масив numpy
masks = masks.numpy()

# змінити тип даних на bool
masks = masks.astype(bool)

# отримати маску для першого об'єкта
mask = masks[0]

print(mask)
# візуалізація маски
mask_img = mask * 255
mask_img = mask_img.astype(np.uint8)

# обрахунок площі об'єкту
area = mask.sum()  # площа в пікселях

pixel_to_meter = 0.0025

area_meter = area * pixel_to_meter
#  <10     – small
#  10-25     – middle
#  >25    – large
if area_meter < 10:
    print(f'Small {area_meter}')
    tumor_type = 'Small'
elif area_meter >25:
    print(f'Large {area_meter}')
    tumor_type = 'Large'
else:
    print(f'Middle {area_meter}')
    tumor_type = 'Middle'


print(f"Площа в пікселях {area}")
print(f"Площа в метрах {area_meter} m2")

# відсоток зайнятої площі від зображення
area_percent = mask.mean()  # середнє арифметичне

print(f"Площа у відсотках {area_percent}")
cv2.imshow(tumor_type, mask_img)
cv2.waitKey(0)