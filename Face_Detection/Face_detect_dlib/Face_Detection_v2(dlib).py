import cv2
import dlib

cnn_detector = dlib.cnn_face_detection_model_v1('mmod_human_face_detector.dat')

cam = cv2.VideoCapture(1)
while True:
    ret, image = cam.read()
    dets = cnn_detector(image, 0)
    for i, det in enumerate(dets):
        face = det.rect
        left = face.left()
        top = face.top()
        right = face.right()
        bottom = face.bottom()

        cv2.rectangle(image, (left, top), (right, bottom), (0, 255, 0), 3)

    cv2.imshow('face', image)

    if cv2.waitKey(1) & 0xff == ord('q'):
        break

cam.release()
cv2.destroyAllWindows()
