import tkinter.messagebox
import face_recognition
import dlib
import tkinter as tk
import time
import cv2
import os
import numpy as np
from PIL import ImageTk, Image
import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore


# --------- Face Recognition -------
class Face_recognition:
    def __init__(self):
        # ----- Variable Define -----
        self.user_index = ''
        self.encode_list = []
        self.Name_list = []
        self.acces_crt = False
        self.now_time = 0
        # self.cnn_detector = dlib.cnn_face_detection_model_v1('../mmod_human_face_detector.dat')

    def Encoding_image(self, index):
        self.user_index = index
        path = '../pic/test_3'
        for file in os.listdir(path):
            if file.split('.')[0] == index:
                self.Name_list.append(file.split('.')[0])
                img = cv2.imread(f'{path}/{file}')
                img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
                encode = face_recognition.face_encodings(img)[0]
                self.encode_list.append(encode)
        print('Encoding Complete')

    def Recognition(self, image):
        img_resize = cv2.resize(image, (0, 0), None, 0.25, 0.25)
        img_RGB = cv2.cvtColor(img_resize, cv2.COLOR_BGR2RGB)

        face_cur_frame = face_recognition.face_locations(img_resize)
        encoding_cur_frame = face_recognition.face_encodings(img_RGB, face_cur_frame)

        for encode_face, face_Loc in zip(encoding_cur_frame, face_cur_frame):
            matches = face_recognition.compare_faces(self.encode_list, encode_face)
            face_dis = face_recognition.face_distance(self.encode_list, encode_face)
            # print(face_dis)
            match_index = np.argmin(face_dis)

            if matches[match_index]:
                name = self.Name_list[match_index]
                if name == self.user_index:
                    if self.now_time == 0:
                        self.now_time = time.time()
                    elif int(time.time() - self.now_time) > 3:
                        print('OK')
                        self.acces_crt = True
                    else:
                        print(int(time.time() - self.now_time))
                        cv2.putText(image, str(int(time.time() - self.now_time)), (480, 100),
                                    cv2.FONT_HERSHEY_COMPLEX, 1, (255, 255, 255), 2)
                else:
                    self.now_time = 0
                y1, x2, y2, x1 = face_Loc
                y1, x2, y2, x1 = y1 * 4, x2 * 4, y2 * 4, x1 * 4
                cv2.rectangle(image, (x1, y1), (x2, y2), (0, 255, 0), 2)
                cv2.rectangle(image, (x1, y2 - 35), (x2, y2), (0, 255, 0), cv2.FILLED)
                cv2.putText(image, name, (x1 + 6, y2 - 6), cv2.FONT_HERSHEY_COMPLEX, 1,
                            (255, 255, 255), 2)
            else:
                '''dets = self.cnn_detector(image, 1)
                for i, det in enumerate(dets):
                    face = det.rect
                    left = face.left()
                    top = face.top()
                    right = face.right()
                    bottom = face.bottom()

                    cv2.rectangle(image, (left, top), (right, bottom), (0, 255, 0), 3)'''
                self.now_time = 0

        return image, self.acces_crt


# --------- Firebase --------
class My_Firebase:
    def __init__(self):
        cred = credentials.Certificate('../robot-arm-55a6f-firebase-adminsdk-uz5oh-0f4ed68310.json')
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

    def get(self, collection, document, ):
        user_ref = self.database.collection(collection)
        doc_ref = user_ref.document(document)
        doc = doc_ref.get()
        doc_id = doc.id
        doc_dict = doc.to_dict()
        return doc_dict

    def delete_data(self, collection, document, ):
        user_ref = self.database.collection(collection)
        doc_ref = user_ref.document(document)
        doc_ref.delete()


# -------- Login GUI --------
class Sign_in:
    def __init__(self):
        # ----- Variable define -----
        self.user_index = ''
        self.detect_flag = False

        # ----- login -----
        # ----- Window Setting -----
        self.window = tk.Tk()
        self.window.geometry('350x230')
        self.window.title('Login')

        # ----- From -----
        self.Label_1 = tk.Label(self.window)
        self.Entry_1 = tk.Entry(self.window)
        self.Label_2 = tk.Label(self.window)
        self.Entry_2 = tk.Entry(self.window)
        self.Cancel_button = tk.Button(self.window)
        self.Login_button = tk.Button(self.window)

        self.login_gui()

        # ----- Recognition -----
        self.detect_window = tk.Tk()
        self.detect_window.title('Face Detection')
        self.detect_window.geometry('645x530')
        # ----- From -----
        self.Label_3 = tk.Label(self.detect_window)
        # self.Canvas_1 = tk.Canvas(self.detect_window)
        if self.detect_flag:
            print('Start Detect')

            self.camera = cv2.VideoCapture(0)
            cam_width = self.camera.get(cv2.CAP_PROP_FRAME_WIDTH)
            cam_height = self.camera.get(cv2.CAP_PROP_FRAME_HEIGHT)
            ret, self.image = self.camera.read()
            self.image_F = Image.fromarray(self.image)
            self.image_tk = ImageTk.PhotoImage(image=self.image_F)
            self.canvas = tk.Canvas(self.detect_window, width=cam_width, height=cam_height, bg='black')
            self.canvas.place(x=0, y=45)
            self.img_canvas = self.canvas.create_image(cam_width / 2 + 2, cam_height / 2 + 2,
                                                       image=self.image_tk)

            self.detect_gui()

    def login_gui(self):
        # ----- Form -----
        self.Label_1.configure(text='User Name:', font=('Times', 16, 'bold'))
        self.Label_1.place(x=110, y=10)

        self.Entry_1.configure(font=('Times', 16, 'bold'))
        self.Entry_1.place(x=60, y=40)

        self.Label_2.configure(text='Password:', font=('Times', 16, 'bold'))
        self.Label_2.place(x=110, y=80)

        self.Entry_2.configure(font=('Times', 16, 'bold'), show='*')
        self.Entry_2.place(x=60, y=110)

        self.Cancel_button.configure(text='Cancel', width=6, font=('Times', 14, 'bold'), command=self.close)
        self.Cancel_button.place(x=40, y=170)

        self.Login_button.configure(text='Login', width=6, font=('Times', 14, 'bold'), command=self.login_system)
        self.Login_button.place(x=240, y=170)

        self.window.mainloop()

    def login_system(self):
        username_now = self.Entry_1.get()
        password_now = self.Entry_2.get()
        if username_now == '' or password_now == '':
            print('Error')
            tkinter.messagebox.showerror(title='Error',
                                         message='UserName or Password Error')
        else:
            data = MF.get('Face Detection', username_now)
            if data is None:
                print('UserName or Password Error')
                tkinter.messagebox.showerror(title='Error',
                                             message='UserName or Password Error')
            else:
                if data['UserName'] == username_now and data['Password'] == password_now:
                    print('Correct')
                    self.user_index = username_now
                    self.detect_flag = True
                    Frc.Encoding_image(self.user_index)
                    self.window.destroy()
                else:
                    tkinter.messagebox.showerror(title='Error',
                                                 message='UserName or Password Error')
                    print('UserName or Password Error')

    # ----- Detection -----
    def detect_gui(self):
        self.Label_3.configure(text='進行臉部辨識...', font=('microsoft yahei', 16, 'bold'))
        self.Label_3.place(x=250, y=10)

        self.canvas.after(1, self.refresh_cam)

        self.detect_window.mainloop()

    def refresh_cam(self):
        ret, self.image = self.camera.read()
        image = cv2.flip(self.image, 1)
        image, brk = Frc.Recognition(image)
        image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        # image = cv2.rectangle(image, (200, 100), (440, 380), (255, 0, 0), 3)

        self.image_F = Image.fromarray(image)
        self.image_tk = ImageTk.PhotoImage(image=self.image_F)
        self.canvas.itemconfig(self.img_canvas, image=self.image_tk)
        if not brk:
            self.canvas.after(1, self.refresh_cam)
        else:
            print('BK')
            self.Label_3.configure(text='辨識成功')
            time.sleep(1)
            self.camera.release()
            cv2.destroyAllWindows()
            self.detect_close()

    def detect_close(self):
        self.detect_window.destroy()

    def close(self):
        self.detect_flag = False
        self.window.destroy()


Frc = Face_recognition()
MF = My_Firebase()
Sign_in()
