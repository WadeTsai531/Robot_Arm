import cv2
import os
import time
import numpy as np
import face_recognition
import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore


class My_Firebase:
    def __init__(self):
        path = 'robot-arm-55a6f-firebase-adminsdk-uz5oh-6c6d288142.json'
        cred = credentials.Certificate(path)
        firebase_admin.initialize_app(cred)
        self.database = firestore.client()

    def set_data(self, collection, document, data_set):
        user_ref = self.database.collection(collection)
        doc_ref = user_ref.document(document)
        doc_ref.set(data_set)

    def update(self, collection, document, data):
        user_ref = self.database.collection(collection)
        doc_ref = user_ref.document(document)
        doc_ref.update(data)

    def get(self, collection, document):
        user_ref = self.database.collection(collection)
        doc_ref = user_ref.document(document)
        doc = doc_ref.get()
        doc_dict = doc.to_dict()
        return doc_dict

    def list(self, collection):
        user_ref = self.database.collection(collection)
        doc_ref = user_ref.document('User_List')
        doc = doc_ref.get()
        doc_dict = doc.to_dict()
        return doc_dict

    def delete_data(self, collection, document):
        user_ref = self.database.collection(collection)
        doc_ref = user_ref.document(document)
        doc_ref.delete()

        user_list = self.list(collection)['User']
        for index, user in enumerate(user_list):
            if user['Name'] == document:
                print('Remove', document)
                user_list.pop(index)
        us_data = {'User': user_list}
        self.set_data(collection, 'User_List', us_data)


class Face_recognition:
    def __init__(self):
        # ----- Variable Define -----
        self.user_index = ''
        self.encode_list = []
        self.Name_list = []
        self.access_crt = False
        self.face_flag = False
        self.now_time = 0

    def Encoding_image(self, image):
        img = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        encode = face_recognition.face_encodings(img)[0]
        self.encode_list.append(encode)
        print('Recognition: Encoding Complete')

    def Recognition(self, image):
        img_resize = cv2.resize(image, (0, 0), None, 0.25, 0.25)
        img_RGB = cv2.cvtColor(img_resize, cv2.COLOR_BGR2RGB)

        face_cur_frame = face_recognition.face_locations(img_resize)
        encoding_cur_frame = face_recognition.face_encodings(img_RGB, face_cur_frame)

        if len(face_cur_frame) != 0:
            for encode_face, face_Loc in zip(encoding_cur_frame, face_cur_frame):
                matches = face_recognition.compare_faces(self.encode_list,
                                                         encode_face,
                                                         tolerance=0.45)
                face_dis = face_recognition.face_distance(self.encode_list, encode_face)
                match_index = np.argmin(face_dis)

                if matches[match_index]:
                    name = self.Name_list[match_index]
                    y1, x2, y2, x1 = face_Loc
                    y1, x2, y2, x1 = y1 * 4, x2 * 4, y2 * 4, x1 * 4
                    cv2.rectangle(image, (x1, y1), (x2, y2), (0, 255, 0), 2)
                    cv2.rectangle(image, (x1, y2 - 35), (x2, y2), (0, 255, 0), cv2.FILLED)
                    cv2.putText(image, name, (x1 + 6, y2 - 6), cv2.FONT_HERSHEY_COMPLEX, 1,
                                (255, 255, 255), 2)

                    if name == self.user_index:
                        if self.now_time == 0:
                            self.now_time = time.time()
                        elif int(time.time() - self.now_time) > 3:
                            print('Recognition: OK')
                            self.now_time = 0
                            self.access_crt = True
                        else:
                            # print(int(time.time() - self.now_time))
                            cv2.putText(image, str(int(time.time() - self.now_time)), (480, 100),
                                        cv2.FONT_HERSHEY_COMPLEX, 1, (0, 0, 255), 2)

                else:
                    y1, x2, y2, x1 = face_Loc
                    y1, x2, y2, x1 = y1 * 4, x2 * 4, y2 * 4, x1 * 4
                    cv2.rectangle(image, (x1, y1), (x2, y2), (0, 255, 0), 2)
                    cv2.rectangle(image, (x1, y2 - 35), (x2, y2), (0, 255, 0), cv2.FILLED)
                    cv2.putText(image, 'Unknown', (x1 + 6, y2 - 6), cv2.FONT_HERSHEY_COMPLEX, 1,
                                (255, 255, 255), 2)
        else:
            self.now_time = 0
        return image, self.access_crt, self.now_time


def Main():
    MF = My_Firebase()
    FRC = Face_recognition()
    lists = MF.get('Face Detection', 'User_List')
    for name in lists['User']:
        print('Name:', name['Name'])
        print('Right:', name['Right'])
        image = cv2.imread('pic/test_3/' + name['Name'] + '.jpg')
        FRC.Encoding_image(image)
        print('Encoding:', FRC.encode_list[0])
        face_encode = FRC.encode_list[0].tolist()
        send_data = {
            'UserName': name['Name'],
            'Password': '12345678',
            'Face encode': face_encode,
            'Authority': name['Right']
        }
        MF.set_data('Face Detection', name['Name'], send_data)


Main()
print('OK')
