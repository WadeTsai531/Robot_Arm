import cv2
import dlib
import math

detector = dlib.get_frontal_face_detector()
predictor = dlib.shape_predictor('shape_predictor_68_face_landmarks.dat')
face_rec_model_path = 'dlib_face_recognition_resnet_model_v1.dat'
face_rec_model = dlib.face_recognition_model_v1(face_rec_model_path)


image_path = '../pic/test_4/temp1.jpg'

image = cv2.imread(image_path)
faces = detector(image)

for face in faces:
    shape = predictor(image, face)
    parts = shape.parts()
    for p in shape.parts():
        cv2.circle(image, (p.x, p.y), 3, (0, 255, 0), -1)

    face_descriptor = face_rec_model.compute_face_descriptor(image, shape)
    print(face_descriptor)

cv2.imshow('image', image)
cv2.waitKey(0)
