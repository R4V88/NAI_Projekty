import time
import cv2

"""
Authors:
    Damian Brzoskowski (s18499)
    Rafał Sochacki (s20047)
Description:
    Program sprawdzający czy użytkownik ogląda reklamy.
        a) Przy braku wykrycia twarzy i oczu jest pokazywany komunikat: "NIE WYKRYWA TWARZY"
        b) Jeżeli po 5 sekundach nadal nie zostanie wykryta twarz lub oczy użytkownik dostanie informacje 'WROC DO OGLADANIA REKLAM'
        c) Jeżeli tylko twarz zostanie wykryta użytkownik dostanie informacje o tym, aby otworzyć oczy
    1. Install:
        pip install opencv-python
    2. Docs/Help
        https://www.geeksforgeeks.org/python-opencv-write-text-on-video/?fbclid=IwAR1uiPjVbhqGTZ4ndJAd72dtIeLtPTriabatcoPCqs07UOFbGXZCU717SjU
        https://docs.opencv.org/3.4/db/d28/tutorial_cascade_classifier.html
        https://www.youtube.com/watch?v=mPCZLOVTEc4
        https://www.youtube.com/watch?v=88HdqNDQsEk
    3. Movie with example:
        https://streamable.com/pgkxct
"""

cap = cv2.VideoCapture(0)
face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
eye_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_eye.xml')
font = cv2.FONT_HERSHEY_SIMPLEX
start = time.time()

while True:
    ret, frame = cap.read()

    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    faces = face_cascade.detectMultiScale(gray, 1.3, 5)

    advertisement_info = False
    show_message = True
    open_eyes = True
    for (x, y, w, h) in faces:
        if w > 0:
            show_message = False
            start = time.time()
        cv2.rectangle(frame, (x, y), (x + w, y + h), (255, 0, 0), 5)
        roi_gray = gray[y:y + w, x:x + w]
        roi_color = frame[y:y + h, x:x + w]
        eyes = eye_cascade.detectMultiScale(roi_gray, 1.3, 5)
        for (ex, ey, ew, eh) in eyes:
            cv2.rectangle(roi_color, (ex, ey), (ex + ew, ey + eh), (0, 255, 0), 5)
            open_eyes = False

    if show_message and time.time() - start > 5:
        cv2.putText(frame, 'WROC DO OGLADANIA REKLAM', (50, 50), font, 1, (5, 150, 255), 2, cv2.LINE_4)
        advertisement_info = True

    if show_message and not advertisement_info:
        cv2.putText(frame, 'NIE WYKRYWA TWARZY', (50, 50), font, 1, (0, 255, 255), 2, cv2.LINE_4)

    if open_eyes and not show_message:
        cv2.putText(frame, 'OTWORZ OCZY', (100, 100), font, 1, (5, 100, 255), 2, cv2.LINE_4)

    cv2.imshow('Kamerka', frame)

    if cv2.waitKey(1) == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()