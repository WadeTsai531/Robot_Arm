import cv2
import dlib

cnn_detector = dlib.cnn_face_detection_model_v1('mmod_human_face_detector.dat')
detector = dlib.get_frontal_face_detector()
predictor = dlib.shape_predictor('shape_predictor_68_face_landmarks.dat')

cam = cv2.VideoCapture(0)
while True:
    ret, image = cam.read()
    # cnn_dets = cnn_detector(image, 0)
    faces = detector(image)

    for k, face in enumerate(faces):
        shape = predictor(image, face)
        print(shape.parts())
        for p in shape.parts():
            cv2.circle(image, (p.x, p.y), 3, (0, 255, 0), -1)

    '''for i, det in enumerate(cnn_dets):
        face = det.rect
        left = face.left()
        top = face.top()
        right = face.right()
        bottom = face.bottom()
        cv2.rectangle(image, (left, top), (right, bottom), (0, 255, 0), 3)'''

    cv2.imshow('face', image)

    if cv2.waitKey(1) & 0xff == ord('q'):
        break

cam.release()
cv2.destroyAllWindows()
