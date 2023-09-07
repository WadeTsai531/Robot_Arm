import cv2
import dlib

detector = dlib.get_frontal_face_detector()

cam = cv2.VideoCapture(0)
while True:
    ret, image = cam.read()
    dets = detector(image, 1)
    for i, det in enumerate(dets):
        left = det.left()
        top = det.top()
        right = det.right()
        bottom = det.bottom()

        cv2.rectangle(image, (left, top), (right, bottom), (0, 255, 0), 3)

    cv2.imshow('face', image)

    if cv2.waitKey(1) & 0xff == ord('q'):
        break

cam.release()
cv2.destroyAllWindows()
