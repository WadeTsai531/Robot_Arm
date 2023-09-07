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
face_path = '../pic/test_2'

for f in glob.glob(os.path.join(face_path, '*.jpg')):
    base = os.path.basename(f)
    candidate.append(os.path.splitext(base)[0])
    img = cv2.imread(f)
    dets = detector(img, 0)
    for k, d in enumerate(dets):
        shape = predictor(img, d)
        face_descriptor = facerec.compute_face_descriptor(img, shape)
        v = np.array(face_descriptor)
        descriptors.append(v)
        for p in shape.parts():
            cv2.circle(img, (p.x, p.y), 3, (0, 255, 0), -1)

    cv2.imshow('image', img)
    cv2.waitKey(0)


