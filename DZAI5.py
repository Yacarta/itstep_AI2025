# # Відкрийте відео з файлу data\lesson7\meter.mp4.
# # Проведіть бінарізацію кадрів та збережіть в новий файл.
# # Можливо очистіть від шуму або наведіть різкість через
# # bilateralFilter
import numpy as np
import utils
import cv2
cap = cv2.VideoCapture("data\lesson7\meter.mp4")
# збереження відео
fps = cap.get(cv2.CAP_PROP_FPS)  # чатота відео
width = cap.get(cv2.CAP_PROP_FRAME_WIDTH)  # ширина кадру
height = cap.get(cv2.CAP_PROP_FRAME_HEIGHT)
resized_width = int(width*0.3)
resized_height = int(width*0.3)
    # # # кодек
fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    # #
writer = cv2.VideoWriter(
        "data\lesson7\meter23.mp4",  # назва файлу
        fourcc,   #  кодек
        fps,      # частота кадрів
        (resized_width, resized_height),   # розмір кадру
        isColor=False  # чи кольорове зображення
    )

while True:
    # отримуєте наступний кадр
    ret, img = cap.read()

    # якщо не вдалось прочитати кадр -- цикл
    if not ret:
        break
    resized_img = cv2.resize(img, None,fx=0.3, fy=0.3)

    # обробка зображення
    gray = cv2.cvtColor(resized_img, cv2.COLOR_BGR2GRAY)
    #  очищеня шумів
    new_img = cv2.bilateralFilter(gray,
                                  d=9,
                                  sigmaColor=75,
                                  sigmaSpace=75,
                                  )
        #  адаптивну бінарізацію
    adaptive = cv2.adaptiveThreshold(new_img,
                                    255,
                                    cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
                                    cv2.THRESH_BINARY,
                                    17,
                                    2,
                                    )

    # показ зображення
    cv2.imshow('adaptive', adaptive)
    writer.write(adaptive)


    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# звільнення пам'яті
writer.release()
cap.release()

