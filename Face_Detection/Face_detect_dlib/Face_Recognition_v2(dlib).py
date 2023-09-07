import cv2
import dlib
import numpy as np


class Face_Recognition:
    def __init__(self):
        self.cam = cv2.VideoCapture(0)
        self.cnn_detector = dlib.cnn_face_detection_model_v1('mmod_human_face_detector.dat')

        self.face_detector = dlib.get_frontal_face_detector()
        self.pose_predictor_68_point = dlib.shape_predictor('shape_predictor_68_face_landmarks.dat')
        self.pose_predictor_5_point = dlib.shape_predictor('shape_predictor_5_face_landmarks.dat')

        face_rec_model_path = 'dlib_face_recognition_resnet_model_v1.dat'
        self.face_encoder = dlib.face_recognition_model_v1(face_rec_model_path)

    def Initial(self):
        image = cv2.imread('../pic/test_2/test1.jpg')
        return self.face_detect(image)

    def face_detect(self, image):
        faces = self.detector(image)
        face_detectors = None
        for k, face in enumerate(faces):
            shape = self.predictor(image, face)
            face_detectors = self.face_rec_model.compute_face_descriptor(image, shape)
        return face_detectors

    def set_vector(self, face_detectors):
        vector = np.array([])
        for i, num in enumerate(face_detectors):
            vector = np.append(vector, num)
        return vector

    def test(self):
        face_bef_vec = self.set_vector(self.Initial())
        while True:
            ret, image = self.cam.read()
            image = cv2.flip(image, 1)
            cnn_det = self.cnn_detector(image, 0)
            for i, det in enumerate(cnn_det):
                face = det.rect
                left = face.left()
                top = face.top()
                right = face.right()
                bottom = face.bottom()
                cv2.rectangle(image, (left, top), (right, bottom), (0, 255, 0), 3)

            faces = self.detector(image)
            face_detectors = None
            for k, face in enumerate(faces):
                shape = self.predictor(image, face)
                face_detectors = self.face_rec_model.compute_face_descriptor(image, shape)

            '''if face_now is not None:
                face_now_vec = self.set_vector(face_now)
                diff = 0
                for i in range(len(face_now_vec)):
                    diff += (face_now_vec[i] - face_bef_vec[i]) ** 2
                diff = np.sqrt(diff)'''

            cv2.imshow('face', image)

            if cv2.waitKey(1) & 0xff == ord('q'):
                break

        self.cam.release()
        cv2.destroyAllWindows()

    def test2(self):
        image = cv2.imread('../pic/kk.jpg')
        cnn_dets = self.cnn_detector(image)
        for i, det in enumerate(cnn_dets):
            face = det.rect
            left = face.left()
            top = face.top()
            right = face.right()
            bottom = face.bottom()
            cv2.rectangle(image, (left, top), (right, bottom), (0, 255, 0), 3)
        cv2.imshow('face', image)
        cv2.waitKey(0)

    def test3(self):
        while True:
            ret, image = self.cam.read()
            image = cv2.flip(image, 1)
            image_RGB = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

            face_cur_frame = self.cnn_detector(image)
            loc_tuple = []
            for face in face_cur_frame:
                css = face.rect
                top = max(css.top(), 0)
                right = min(css.right(), image.shape[1])
                bottom = min(css.bottom(), image.shape[0])
                left = max(css.left(), 0)
                loc_tuple.append((top, right, bottom, left))
                cv2.rectangle(image, (left, top), (right, bottom), (0, 255, 0), 3)

            face_locations = 0
            if loc_tuple != 0:
                for face_loc in loc_tuple:
                    face_locations = dlib.rectangle(face_loc[3], face_loc[0], face_loc[1], face_loc[2])
                    face_det = self.pose_predictor_68_point(image_RGB, face_locations)
                    face_compute = self.face_encoder.compute_face_descriptor(image_RGB, face_det, 1)
                    vector = np.array(face_compute)
            cv2.imshow('image', image)

            if cv2.waitKey(1) & 0xff == ord('q'):
                self.cam.release()
                cv2.destroyAllWindows()
                break


FCR = Face_Recognition()
print('start')
FCR.test3()
print('stop')
