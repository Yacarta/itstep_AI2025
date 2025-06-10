# Відкрийте відео data/lesson_pose/squat.mp4
# Ваша задача рахувати кількість присідань.
# Отримайте перший кадр та виділіть основні точки.
# Отримайте координати 3-ох точок ноги
# Визначте кут між цими трьома точками. Скористайтесь
# функцією utils.get_angle(x1, y1, x2, y2, x3, y3) де x2, y2 –
# координати коліна(центральна точка)
# Запустіть відео та добавте на сам кадр кут згинання ніг.
# Визначіть нижню межу кута(якщо людина опустилась
# нижче  вважаємо що вона достатньо опустилась) та верхню
# межу кута(якщо людина піднялась вище вважаємо що вона
# достатньо піднялась)
# Добавте кількість присідань та
# кут на кожен кадр.

import cv2
import ultralytics



model = ultralytics.YOLO('yolo11n-pose.pt')

cap = cv2.VideoCapture('data/lesson_pose/squat.mp4')

import numpy as np

def get_angle(x1, y1, x2, y2, x3, y3):
    a = np.array([x1, y1])
    b = np.array([x2, y2])
    c = np.array([x3, y3])

    ab = a - b
    cb = c - b

    dot = ab @ cb
    norm_ab = (ab @ ab) ** 0.5
    norm_cb = (cb @ cb) ** 0.5
    angle = np.arccos(dot / norm_ab / norm_cb)
    angle = angle / np.pi * 180

    return angle

red,imag = cap.read()
imag = cv2.resize(imag,None,fx=0.5,fy=0.5)
results = model.predict(imag)
res1 = results[0]
xy = res1.keypoints.xy.numpy()[0]
xy = xy.astype(int)
xknee, yknee = xy[14]




res_knee = cv2.circle(
    imag,  # зображення на якому намалювати коло
    (xknee, yknee),  # координати центру кола
    10,       # радіус у пікселях
    (0, 255, 0),  # колір у bgr форматі(тут -- зелений)
    -1      # товщина лінії(-1 -- запоанити коло повністю)
)
xt, yt = xy[12]
res_t = cv2.circle(
    imag,  # зображення на якому намалювати коло
    (xt, yt),  # координати центру кола
    10,       # радіус у пікселях
    (0, 255, 0),  # колір у bgr форматі(тут -- зелений)
    -1      # товщина лінії(-1 -- запоанити коло повністю)
)

xstop, ystop = xy[16]
res_stop = cv2.circle(
    imag,  # зображення на якому намалювати коло
    (xstop, ystop),  # координати центру кола
    10,       # радіус у пікселях
    (0, 255, 0),  # колір у bgr форматі(тут -- зелений)
    -1      # товщина лінії(-1 -- запоанити коло повністю)
)


cv2.imshow("", res_knee)
cv2.imshow("", res_t)
cv2.imshow("", res_stop)
cv2.waitKey(0)

count = 0
stage = None
lower_angle = 70
upper_angle = 160

while True:
    red, imag = cap.read()
    if not red:
        break
    imag = cv2.resize(imag, None, fx=0.5, fy=0.5)
    results = model.predict(imag)
    res1 = results[0]
    xy = res1.keypoints.xy.numpy()[0]
    xy = xy.astype(int)
    xknee, yknee = xy[14]

    res_img = cv2.circle(
        imag,  # зображення на якому намалювати коло
        (xknee, yknee),  # координати центру кола
        10,  # радіус у пікселях
        (0, 255, 0),  # колір у bgr форматі(тут -- зелений)
        -1  # товщина лінії(-1 -- запоанити коло повністю)
    )
    xt, yt = xy[12]
    res_img = cv2.circle(
        imag,  # зображення на якому намалювати коло
        (xt, yt),  # координати центру кола
        10,  # радіус у пікселях
        (0, 255, 0),  # колір у bgr форматі(тут -- зелений)
        -1  # товщина лінії(-1 -- запоанити коло повністю)
    )

    xstop, ystop = xy[16]
    res_img = cv2.circle(
        imag,  # зображення на якому намалювати коло
        (xstop, ystop),  # координати центру кола
        10,  # радіус у пікселях
        (0, 255, 0),  # колір у bgr форматі(тут -- зелений)
        -1  # товщина лінії(-1 -- запоанити коло повністю)
    )
    angle = int(get_angle(xt,yt, xknee, yknee, xstop, ystop))
    if angle < lower_angle:
        stage = 'down'
    if angle > upper_angle and stage == 'down':
        stage = 'up'
        count += 1


    cv2.line(imag, (xt, yt), (xknee, yknee), (255, 0, 0), 2)
    cv2.line(imag, (xknee, yknee), (xstop, ystop), (255, 0, 0), 2)

    # Виводимо кут
    cv2.putText(imag, f'Angle: {angle}', (50, 50),
                cv2.FONT_HERSHEY_SIMPLEX, 1.5, (0, 0, 255), 2)

    # Виводимо кількість присідань
    cv2.putText(imag, f'Squats: {count}', (50, 100),
                cv2.FONT_HERSHEY_SIMPLEX, 1.5, (0, 255, 0), 2)

    cv2.imshow('Squat Counter', imag)


    cv2.imshow("", res_img)



    if cv2.waitKey(1) & 0xFF == ord('q'):
        break


cv2.waitKey(0)



