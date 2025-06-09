
# Завдання 1
# Відкрийте відео з файлу data\lesson8\meetings.mp4
#Застосуйте детекцію та виведіть результат, підберіть
#параметри
#Можете змінити розмір кадру для кращої візуалізації
#cv2.resize()
#Завдання 2
#Відкрийте відео з файлу data\lesson8\meetings.mp4
#Застосуйте детекцію та почніть показувати відео з
#моменту, коли людей стало 5
import ultralytics
import cv2

# дістати перший кадр з відео
cap = cv2.VideoCapture("data\lesson8\meetings.mp4")

# використання моделі
model = ultralytics.YOLO("yolov8n.pt")


while True:
    ret, img = cap.read()

    if not ret:
        break
    resized_img = cv2.resize(img, None, fx=0.3, fy=0.3)

    results = model.predict(
        resized_img,
        conf=0.25,  # мінімальний відсоток з яким можна визначити об'єкт
        iou=0.75,  # якщо для двох рамок iuo менший за це число, то вважаємо що це 2 різних об'єкта
        classes=[0]  # індекси класів(тип об'єктів) які будуть детектитись

    )

    result = results[0]

    result_img = result.plot()

    cv2.imshow('detection', result_img)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
# #Завдання 2
# #Відкрийте відео з файлу data\lesson8\meetings.mp4
# #Застосуйте детекцію та почніть показувати відео з
# #моменту, коли людей стало 5

while True:
    ret, img = cap.read()

    if not ret:
        break
    resized_img = cv2.resize(img, None, fx=0.3, fy=0.3)

    results = model.predict(
        resized_img,
        conf=0.25,  # мінімальний відсоток з яким можна визначити об'єкт
        iou=0.75,  # якщо для двох рамок iuo менший за це число, то вважаємо що це 2 різних об'єкта
        classes=[0]  # індекси класів(тип об'єктів) які будуть детектитись

    )
    result = results[0]
    if result and result.boxes is not None:
        people = len(result.boxes)
    if people >= 5:
        result_img = result.plot()

        cv2.imshow('people', result_img)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break


cap.release()
