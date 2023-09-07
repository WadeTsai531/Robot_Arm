import cv2
import numpy as np
import face_recognition

shimo_img = face_recognition.load_image_file('pic/shimo/shimo_1.jpg')
shimo_img = cv2.cvtColor(shimo_img, cv2.COLOR_BGR2RGB)

shimo_img_test = face_recognition.load_image_file('pic/kaya/kaya_0.jpg')
shimo_img_test = cv2.cvtColor(shimo_img_test, cv2.COLOR_BGR2RGB)

faceloc = face_recognition.face_locations(shimo_img)[0]
encodeshimo = face_recognition.face_encodings(shimo_img)[0]
cv2.rectangle(shimo_img, (faceloc[3], faceloc[0]), (faceloc[1], faceloc[2]), (255, 0, 255), 2)

faceloc_test = face_recognition.face_locations(shimo_img_test)[0]
encodeshimo_test = face_recognition.face_encodings(shimo_img_test)[0]
cv2.rectangle(shimo_img_test,
              (faceloc_test[3], faceloc_test[0]),
              (faceloc_test[1], faceloc_test[2]),
              (255, 0, 255), 2)

results = face_recognition.compare_faces([encodeshimo], encodeshimo_test)
print(results)

cv2.imshow('shimo', shimo_img)
cv2.imshow('shimo test', shimo_img_test)
cv2.waitKey(0)
