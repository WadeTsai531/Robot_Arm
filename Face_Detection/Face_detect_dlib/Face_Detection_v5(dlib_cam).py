import glob
import dlib
import os
import cv2
import numpy as np

detector = dlib.get_frontal_face_detector()
predictor = dlib.shape_predictor('shape_predictor_68_face_landmarks_GTX.dat')

face_rec_model_path = 'dlib_face_recognition_resnet_model_v1.dat'
facerec = dlib.face_recognition_model_v1(face_rec_model_path)

descriptors = []
candidate = []

cam = cv2.VideoCapture(0)

while True:
    ret, image = cam.read()

    det = detector(image, 0)
    for k, d in enumerate(det):
        shape = predictor(image, d)
        face_descriptor = facerec.compute_face_descriptor(image, shape)
        for p in shape.parts():
            cv2.circle(image, (p.x, p.y), 3, (0, 255, 0), -1)

    cv2.imshow('image', image)

    if cv2.waitKey(1) & 0xff == ord('q'):
        break
