import cv2

path = 'haarcascade_frontalface_default.xml'
face_cascade = cv2.CascadeClassifier(path)

cap = cv2.VideoCapture(0)

while True:
    frame, image = cap.read()
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    faces = face_cascade.detectMultiScale(gray, 1.1, 3)
    for (x, y, w, h) in faces:
        cv2.rectangle(image, (x, y), (x+w, y+h), (255, 0, 0), 2)

    cv2.imshow('image', image)

    if cv2.waitKey(1) & 0xff == ord('q'):
        break

cap.release()
