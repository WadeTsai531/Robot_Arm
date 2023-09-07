import math
import os
import time
import tkinter as tk
import tkinter.messagebox
from tkinter import ttk

import cv2
import face_recognition
import firebase_admin
import numpy as np
import serial.tools.list_ports
from PIL import ImageTk, Image
from firebase_admin import credentials
from firebase_admin import firestore

from Track_package import Tracking_model_v3


# ---------------- Function ----------------
def Data_Transform(data_in):
    if data_in >= 100:
        data_send = str(data_in)
    elif 100 > data_in >= 10:
        data_send = '0' + str(data_in)
    else:
        data_send = '00' + str(data_in)
    return data_send


# ---------------- Program ----------------
class Serial_System:
    def __init__(self):
        # -------- Variable define --------
        self.ser = serial.Serial()
        self.list_of_port = []
        self.serial_open = False

        # -------- Scan Serial Port --------
        self.Scan_Serial_Port()

        # -------- Object define --------
        self.label = None
        self.combobox = None
        self.Connect_button = None
        self.Disconnect_button = None

    def GUI(self, window, x, y):
        self.label = tk.Label(window, text='Select Serial Port:', font=('Times', 16, 'bold'))
        self.label.place(x=x, y=y)

        self.combobox = ttk.Combobox(window, value=self.list_of_port,
                                     font=('Times', 14, 'bold'))
        self.combobox.place(x=x, y=y + 30)

        self.Connect_button = tk.Button(window, text='Connect', width=10,
                                        font=('Times', 14, 'bold'),
                                        command=self.Connect_Serial_Port)
        self.Connect_button.place(x=x + 240, y=y)

        self.Disconnect_button = tk.Button(window, text='Disconnect', width=10,
                                           font=('Times', 14, 'bold'),
                                           command=self.Disconnect_Serial_Port)
        self.Disconnect_button.place(x=x + 240, y=y + 50)

    def Scan_Serial_Port(self):
        list_ports = serial.tools.list_ports.comports()
        print('Scan')
        for port in list_ports:
            self.list_of_port.append(port.name)
            print(port.name)

    def Connect_Serial_Port(self):
        print('Connecting .....')

        try:
            self.serial_open = True
            self.ser.port = self.combobox.get()
            self.ser.open()
            print('Connect to device')
        except EnvironmentError:
            print('Connect Fail !!!!')

    def Disconnect_Serial_Port(self):
        print('Disconnect Serial Port')
        self.serial_open = False
        self.ser.close()

    def Transmit_value(self, port, value):
        send_data = port + Data_Transform(int(value)) + '/'

        if self.serial_open:
            print('Serial Value:', send_data)
            self.ser.write(send_data.encode('utf-8'))
        time.sleep(0.001)

    def Transmit_msg(self, port):
        send_data = port + '/'

        if self.serial_open:
            print('Serial Msg:', send_data)
            self.ser.write(send_data.encode('utf-8'))
        time.sleep(0.005)


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


class Face_recognition:
    def __init__(self):
        # ----- Variable Define -----
        self.user_index = ''
        self.encode_list = []
        self.Name_list = []
        self.acces_crt = False
        self.face_flag = False
        self.now_time = 0

    def Encoding_image(self, index):
        self.user_index = index
        self.Name_list = []
        self.encode_list = []
        path = 'test_3'
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

        if len(face_cur_frame) != 0:
            for encode_face, face_Loc in zip(encoding_cur_frame, face_cur_frame):
                matches = face_recognition.compare_faces(self.encode_list, encode_face)
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
                            print('OK')
                            self.now_time = 0
                            self.acces_crt = True
                        else:
                            print(int(time.time() - self.now_time))
                            cv2.putText(image, str(int(time.time() - self.now_time)), (480, 100),
                                        cv2.FONT_HERSHEY_COMPLEX, 1, (255, 255, 255), 2)
        else:
            self.now_time = 0
        return image, self.acces_crt


class Login_System:
    def __init__(self, cam_index):
        # ----- Variable define -----
        self.user_index = ''
        self.detect_flag = False
        self.cancel_flag = True
        self.cam_index = cam_index

        # ----- Object define -----
        self.camera = None
        self.image = None
        self.window = None
        self.detect_window = None
        self.Label_1 = None
        self.Label_2 = None
        self.Label_3 = None
        self.Entry_1 = None
        self.Entry_2 = None
        self.Cancel_button = None
        self.Login_button = None

        # ----- Camera -----
        self.image_F = None
        self.image_tk = None
        self.canvas = None
        self.img_canvas = None

    # ----- login -----
    def GUI(self):
        self.cancel_flag = True
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
        if not self.cancel_flag:
            self.detect()

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

        self.Cancel_button.configure(text='Cancel', width=6, font=('Times', 14, 'bold'),
                                     command=self.close)
        self.Cancel_button.place(x=40, y=170)

        self.Login_button.configure(text='Login', width=6, font=('Times', 14, 'bold'),
                                    command=self.Comparison)
        self.Login_button.place(x=240, y=170)

        self.window.mainloop()

    def Comparison(self):
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
                    self.cancel_flag = False
                    FRC.Encoding_image(self.user_index)
                    self.window.destroy()
                else:
                    tkinter.messagebox.showerror(title='Error',
                                                 message='UserName or Password Error')
                    print('UserName or Password Error')

    def detect_gui(self):
        self.Label_3.configure(text='進行臉部辨識...', font=('microsoft yahei', 16, 'bold'))
        self.Label_3.place(x=250, y=10)

        self.canvas.after(1, self.refresh_cam)

        self.detect_window.mainloop()

    def detect(self):
        # ----- Recognition -----
        self.detect_window = tk.Tk()
        self.detect_window.title('Face Detection')
        self.detect_window.geometry('645x530')
        # ----- From -----
        self.Label_3 = tk.Label(self.detect_window)
        # self.Canvas_1 = tk.Canvas(self.detect_window)
        self.camera = cv2.VideoCapture(self.cam_index)
        if self.detect_flag:
            print('Start Detect')
            cam_width = self.camera.get(cv2.CAP_PROP_FRAME_WIDTH)
            cam_height = self.camera.get(cv2.CAP_PROP_FRAME_HEIGHT)

            ret, image = self.camera.read()

            self.image_F = Image.fromarray(image)
            self.image_tk = ImageTk.PhotoImage(self.image_F)

            self.canvas = tk.Canvas(self.detect_window, width=cam_width, height=cam_height, bg='black')
            self.canvas.place(x=0, y=45)
            self.img_canvas = self.canvas.create_image(cam_width / 2 + 2, cam_height / 2 + 2,
                                                       image=self.image_tk)
            self.detect_gui()

    def refresh_cam(self):
        ret, image = self.camera.read()
        image = cv2.flip(image, 1)
        image, brk = FRC.Recognition(image)
        image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        # image = cv2.rectangle(image, (200, 100), (440, 380), (255, 0, 0), 3)

        self.image_F = Image.fromarray(image)
        self.image_tk = ImageTk.PhotoImage(image=self.image_F)
        self.canvas.itemconfig(self.img_canvas, image=self.image_tk)
        if not brk:
            self.canvas.after(1, self.refresh_cam)
        else:
            FRC.acces_crt = False
            print('BK')
            self.Label_3.configure(text='辨識成功')
            self.camera.release()
            cv2.destroyAllWindows()
            self.detect_close()

    def detect_close(self):
        self.detect_window.destroy()

    def close(self):
        self.detect_flag = False
        self.window.destroy()


class Video_Cam:
    def __init__(self, window):
        self.cap_flag = False
        self.cap_value = 0
        self.time_now = 0
        self.photo_name = ''
        self.save_img = None

        self.camera = cv2.VideoCapture(1)  # <<<<<<<<<<<<=======
        cam_width = self.camera.get(cv2.CAP_PROP_FRAME_WIDTH)
        cam_height = self.camera.get(cv2.CAP_PROP_FRAME_HEIGHT)
        ret, self.image = self.camera.read()
        self.image_F = Image.fromarray(self.image)
        self.image_tk = ImageTk.PhotoImage(image=self.image_F)
        self.canvas = tk.Canvas(window, width=cam_width, height=cam_height, bg='black')
        self.canvas.place(x=1, y=1)
        self.img_canvas = self.canvas.create_image(cam_width / 2 + 2, cam_height / 2 + 2,
                                                   image=self.image_tk)
        self.canvas_run = self.canvas.after(1, self.refresh_cam)

    def refresh_cam(self):
        ret, self.image = self.camera.read()
        image = cv2.flip(self.image, 1)
        image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        image = cv2.rectangle(image, (200, 100), (440, 380), (255, 0, 0), 3)
        if self.cap_value != 0:
            if self.cap_value == 1:
                self.time_now = time.time()
                self.cap_value = 2

            if int(time.time() - self.time_now) > 0:
                self.cap_value += 1
                self.time_now = time.time()

            if self.cap_value - 2 == 3 and not self.cap_flag:
                self.cap_flag = True
                self.Capture(self.photo_name, False)

            if self.cap_value > 4:
                image = cv2.putText(image, 'OK!!', (540, 80),
                                    cv2.FONT_HERSHEY_TRIPLEX, 1, (255, 0, 0), 3)
            else:
                image = cv2.putText(image, str(5 - self.cap_value), (540, 80),
                                    cv2.FONT_HERSHEY_TRIPLEX, 1, (255, 0, 0), 3)

            if self.cap_value >= 6:
                self.cap_flag = False
                self.cap_value = 0

        self.image_F = Image.fromarray(image)
        self.image_tk = ImageTk.PhotoImage(image=self.image_F)
        self.canvas.itemconfig(self.img_canvas, image=self.image_tk)
        self.canvas_run = self.canvas.after(1, self.refresh_cam)

    def stop_vision(self):
        self.canvas.after_cancel(self.canvas_run)

    def Capture(self, name, state):
        print('save picture')
        if state:
            '''file_name = fd.asksaveasfile(initialfile='Sample.jpg', defaultextension='.jpg',
                                                                         filetypes=[('All Files', '*.*')])'''
            cv2.imwrite('test_3/' + name + '.jpg', self.save_img)
        elif self.cap_flag:
            self.save_img = self.image

        else:
            self.photo_name = name
            self.cap_value = 1


class Logout_Create_System:
    user = ''

    def __init__(self):
        # ----- Variable -----
        self.in_out = True

        self.username = ''
        self.password = ''
        self.username_flag = False
        self.password_flag = False
        self.capture_flag = False
        self.cap_image = None
        self.cap_name = ''

        # ----- Object define -----
        self.Logout_button = None
        self.Create_account_button = None
        self.Delete_button = None
        self.button_2 = None
        self.button_c_1 = None
        self.Text_check = None
        self.user_entry = None
        self.pass_entry = None
        self.window = None
        self.capture = None
        self.run = None

    def GUI(self, window, x, y):
        self.Logout_button = tk.Button(window, text='Logout', width=7,
                                       font=('Times', 13, 'bold'))
        self.Logout_button.place(x=x + 100, y=y)

        self.Create_account_button = tk.Button(window, text='Create', width=7,
                                               font=('Times', 13, 'bold'))
        self.Create_account_button.place(x=x, y=y)

        self.Delete_button = tk.Button(window, text='Delete', width=7,
                                       font=('Times', 13, 'bold'))
        self.Delete_button.place(x=x + 100, y=y + 40)

    def Create_Account(self):
        # --------- Tkinter ---------
        self.window = tk.Tk()
        self.window.geometry('860x485')
        self.window.title('Register Account')
        self.window.resizable(width=False, height=False)

        # --------- Form Design ---------
        vision_canvas = tk.Canvas(self.window, width=640, height=480, bg='black')
        vision_canvas.place(x=0, y=1)

        # ------- Title -------
        label_0 = tk.Label(self.window, text='Register Account',
                           font=('Times', 18, 'bold'))
        label_0.place(x=655, y=5)

        # -------- Username & Password -----------------
        password_y = 40
        frame = tk.Frame(self.window, relief=tk.RAISED, borderwidth=3)
        frame.place(x=645, y=password_y)

        canvas_1 = tk.Canvas(frame, width=200, height=150, bg='#E1E1E1')
        canvas_1.pack()

        label_1 = tk.Label(self.window, text='請輸入帳號名稱及密碼:', bg='#E1E1E1',
                           font=('microsoft yahei', 12, 'bold'))
        label_1.place(x=650, y=password_y + 5)

        label_2 = tk.Label(self.window, text='Username:', bg='#E1E1E1',
                           font=('Times', 16, 'bold'))
        label_2.place(x=650, y=password_y + 30)

        label_2 = tk.Label(self.window, text='(輸入至少4個字)', bg='#E1E1E1',
                           font=('microsoft yahei', 9, 'bold'))
        label_2.place(x=752, y=password_y + 36)

        self.user_entry = tk.Entry(self.window, width=19,
                                   font=('Times', 12, 'bold'))
        self.user_entry.place(x=650, y=password_y + 60)

        label_3 = tk.Label(self.window, text='Password:', bg='#E1E1E1',
                           font=('Times', 16, 'bold'))
        label_3.place(x=650, y=password_y + 90)

        label_2 = tk.Label(self.window, text='(輸入至少8個字)', bg='#E1E1E1',
                           font=('microsoft yahei', 9, 'bold'))
        label_2.place(x=752, y=password_y + 96)

        self.pass_entry = tk.Entry(self.window, width=19, show='*',
                                   font=('Times', 12, 'bold'))
        self.pass_entry.place(x=650, y=password_y + 120)

        # ----------- Capture --------------
        capture_y = 210
        frame_capture = tk.Frame(self.window, relief=tk.RAISED, borderwidth=3)
        frame_capture.place(x=645, y=capture_y)

        canvas_2 = tk.Canvas(frame_capture, width=200, height=110, bg='#E1E1E1')
        canvas_2.pack()

        label_c_1 = tk.Label(self.window, text='1. 將臉對準方格內\n'
                                               '2. 按下截圖按鈕',
                             bg='#E1E1E1', justify=tk.LEFT,
                             font=('microsoft yahei', 12, 'bold'))
        label_c_1.place(x=650, y=capture_y + 5)

        self.button_c_1 = tk.Button(self.window, text='Capture', width=15,
                                    font=('Times', 16, 'bold'), state=tk.DISABLED,
                                    command=self.Cap)
        self.button_c_1.place(x=655, y=capture_y + 60)

        # ----------- Create & Check --------------
        check_y = 340

        button_1 = tk.Button(self.window, text='Cancel', width=6,
                             font=('Times', 14, 'bold'), command=self.close)
        button_1.place(x=650, y=440)

        self.button_2 = tk.Button(self.window, text='Register', width=6, state=tk.DISABLED,
                                  font=('Times', 14, 'bold'), command=self.register)
        self.button_2.place(x=780, y=440)

        self.Text_check = tk.Text(self.window, width=20, height=4,
                                  font=('Times', 14, 'bold'))
        self.Text_check.place(x=645, y=check_y)

        self.Text_check.insert('insert', 'Username:  \n')
        self.Text_check.insert('insert', 'Password:  \n')
        self.Text_check.insert('insert', 'Face Capture:  \n')

        self.capture = Video_Cam(self.window)
        self.run = self.Text_check.after(1, self.check)

        self.window.mainloop()

    def check(self):
        if self.capture.cap_flag:
            self.capture_flag = True

        if self.username_flag and self.password_flag and self.capture_flag:
            self.button_2.config(state=tk.NORMAL)

        # Check username
        if self.user_entry.get() != '' and len(self.user_entry.get()) > 3:
            self.username_flag = True
            self.username = self.user_entry.get()
            self.button_c_1.config(state=tk.NORMAL)
            self.Text_check.delete('1.10', '1.17')
            self.Text_check.insert('1.10', 'OK!')

        # Check password
        if self.pass_entry.get() != '' and len(self.pass_entry.get()) > 7:
            self.password_flag = True
            self.password = self.pass_entry.get()
            self.Text_check.delete('2.10', '2.17')
            self.Text_check.insert('2.10', 'OK!')

        if self.capture_flag:  # Check Capture
            self.Text_check.delete('3.14', '3.21')
            self.Text_check.insert('3.14', 'OK!')

        self.run = self.Text_check.after(1, self.check)

    def Cap(self):
        self.capture.Capture('', False)

    def register(self):
        if MF.get('Face Detection', self.username) is None:
            print('Create New Account')
            send_data = {
                'UserName': self.username,
                'Password': self.password,
                'Pic name': self.user_entry.get() + '.jpg'
            }
            MF.set_data('Face Detection', self.username, send_data)
            self.capture.Capture(self.user_entry.get(), True)
            print(self.username)
            print(self.password)
            self.Text_check.insert('4.0', 'Upload Successful')
            self.close()
        else:
            print('Account is exist')
            self.Text_check.insert('4.0', 'Account is exist !!!')

    def close(self):
        self.Text_check.after_cancel(self.run)
        self.capture.stop_vision()
        self.window.destroy()


class Vision_System:
    def __init__(self, cam_index):
        # ----- Variable -----
        self.canvas_run = None
        self.vision_close = False
        self.canvas = None
        self.img_canvas = None
        self.image_tk = None
        self.image_F = None
        self.Tracking_Enable = False
        self.Tracking_System = Hand_Tracking_System(0.6, 0.8)

        # ----- Camera -----
        self.camera = None
        self.cam_index = cam_index

    def GUI(self, window):
        self.camera = cv2.VideoCapture(self.cam_index)
        cam_width = self.camera.get(cv2.CAP_PROP_FRAME_WIDTH)
        cam_height = self.camera.get(cv2.CAP_PROP_FRAME_HEIGHT)

        ret, image = self.camera.read()

        self.image_F = Image.fromarray(image)
        self.image_tk = ImageTk.PhotoImage(self.image_F)

        self.canvas = tk.Canvas(window, width=cam_width, height=cam_height, bg='black')
        self.canvas.place(x=5, y=5)
        self.img_canvas = self.canvas.create_image(cam_width / 2 + 2, cam_height / 2 + 2,
                                                   image=self.image_tk)
        self.canvas_run = self.canvas.after(1, self.vis_cam)

    def vis_cam(self):
        ret, image = self.camera.read()
        if self.Tracking_Enable:
            image = self.Tracking_System.digital_finger(image)
        else:
            image = self.Tracking_System.nor_tracking(image)
        image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)

        self.image_F = Image.fromarray(image)
        self.image_tk = ImageTk.PhotoImage(self.image_F)

        self.canvas.itemconfig(self.img_canvas, image=self.image_tk)
        self.canvas_run = self.canvas.after(1, self.vis_cam)

    def stop_vision(self):
        self.canvas.after_cancel(self.canvas_run)


class Hand_Tracking_System(Tracking_model_v3.Media):
    def __init__(self, mdc, mtc):
        super().__init__(mdc, mtc)
        self.check_time = 0
        self.flag = {'Right': False,
                     'Left': False,
                     'Middle': True}
        self.Num = {'Right': None,
                    'Left': None}

    # ----- Close >> Open -----
    def nor_tracking(self, image):
        image = super().tracking(image)
        my_list = self.my_dir

        def finger_point(point, R_L=0):
            x, y = my_list[R_L][1][point][1], \
                   my_list[R_L][1][point][2]
            cv2.circle(image, (x, y), 12, (255, 0, 255), cv2.FILLED)
            return x, y

        def Finger_Recog(RL_index):
            def distance(point_1, point_2):
                x1, y1 = finger_point(point_1)
                x2, y2 = finger_point(point_2)
                dist = math.sqrt((x1 - x2) ** 2 + (y1 - y2) ** 2)
                return dist

            def dist_comp(point_1, point_2):
                dist_1 = distance(point_1, point_2)
                dist_2 = distance(point_1 + 1, point_2)
                if dist_2 > dist_1:
                    return False
                else:
                    return True

            recog = []
            T_dist_1 = distance(4, 13)
            T_dist_2 = distance(4, 5)
            if T_dist_2 + 10 > T_dist_1 or T_dist_2 < 20:
                recog.append(False)
            else:
                recog.append(True)
            finger = [[5, 8], [9, 12], [13, 16], [17, 20]]
            for num in finger:
                recog.append(dist_comp(num[0], num[1]))

            if recog == [True, True, False, False, True]:
                if self.check_time == 0:
                    self.check_time = time.time()
                elif time.time() - self.check_time > 4:
                    if Vision.Tracking_Enable:
                        print('Close')
                        Vision.Tracking_Enable = False
                    else:
                        print('Open')
                        Vision.Tracking_Enable = True
                    self.check_time = 0
                else:
                    print(time.time() - self.check_time)
            else:
                self.check_time = 0

        if len(my_list) != 0:
            if len(my_list) > 1:
                index_R = 0
                for kn in range(len(my_list)):
                    if my_list[kn][0] == 'Right':
                        index_R = kn
                    Finger_Recog(index_R)
            else:
                if my_list[0][0] == 'Right':
                    Finger_Recog(0)

        return image

    # ----- Open >> Close -----
    def digital_finger(self, image):
        image = super().tracking(image)
        my_list = self.my_dir
        finger_list = [Thumb,
                       Index_Finger,
                       Middle_Finger,
                       Ring_Finger,
                       Pinky,
                       Arm]

        if len(my_list) != 0:
            def finger_point(point, R_L=0):
                x, y = my_list[R_L][1][point][1], \
                       my_list[R_L][1][point][2]
                cv2.circle(image, (x, y), 12, (255, 0, 255), cv2.FILLED)
                return x, y

            def Finger_up_down(RL_index):
                def distance(finger_index):
                    L = []
                    st = []
                    for point in range(1, 11):
                        x, y = finger_point(point * 2, finger_index)
                        L.append([x, y])
                    st.append(abs(L[0][0]) - abs(L[1][0]))
                    for k in range(2, 9, 2):
                        st.append(abs(L[k][1]) - abs(L[k + 1][1]))
                    return st

                finger_detect = []
                finger_distance = distance(RL_index)
                for index, function_name in enumerate(finger_list[:5]):
                    if finger_distance[index] > 13:
                        finger_detect.append(True)
                        function_name.Vision_function(130)
                    elif finger_distance[index] < -13:
                        finger_detect.append(False)
                        function_name.Vision_function(20)

                if finger_detect == [True, True, False, False, True]:
                    if self.check_time == 0:
                        self.check_time = time.time()
                    elif time.time() - self.check_time > 4:
                        if Vision.Tracking_Enable:
                            print('Close')
                            Vision.Tracking_Enable = False

                            for function_name in finger_list:
                                function_name.Reset(function_name.label_text)
                            Serial.Transmit_msg('S')

                        self.check_time = 0
                    else:
                        print(time.time() - self.check_time)
                else:
                    self.check_time = 0

            def Arm_up_down(index):
                x, y = finger_point(9, index)
                if 138 <= abs(y) <= 380:
                    finger_list[5].Vision_function(130 - int((380 - abs(y)) * (13 / 24)))

            def Slide(index):
                px, py = finger_point(9, index)
                Rx = 200
                Lx = 440
                cv2.line(image, (Rx, 0), (Rx, 480), (255, 0, 0), 2)
                cv2.line(image, (Lx, 0), (Lx, 480), (255, 0, 0), 2)
                if Rx < px < Lx:
                    if not self.flag['Middle']:
                        self.flag['Middle'] = True
                        print('Middle')
                        Serial.Transmit_msg('S')
                else:
                    if self.flag['Middle']:
                        self.flag['Middle'] = False

                if px > Lx:
                    if not self.flag['Right']:
                        self.flag['Right'] = True
                        print('Right')
                        Serial.Transmit_msg('R')
                else:
                    if self.flag['Right']:
                        self.flag['Right'] = False

                if px < Rx:
                    if not self.flag['Left']:
                        self.flag['Left'] = True
                        print('Left')
                        Serial.Transmit_msg('L')
                else:
                    if self.flag['Left']:
                        self.flag['Left'] = False

            # -------- Running --------
            if len(my_list) > 1:
                index_R = 0
                for kn in range(len(my_list)):
                    if my_list[kn][0] == 'Right':
                        index_R = kn
                    Arm_up_down(index_R)
                    Slide(index_R)
                    Finger_up_down(index_R)

            else:
                if my_list[0][0] == 'Right':
                    Arm_up_down(0)
                    Slide(0)
                    Finger_up_down(0)

        return image


class Finger_System:
    def __init__(self, text, port):
        # -------- Variable define --------
        self.label_text = text
        self.transmit_port = port

        # -------- Object define --------
        self.x = None
        self.y = None
        self.sub_label = None
        self.sub_spinbox = None
        self.sub_scale = None
        self.deg = None

    def GUI(self, finger_window, x, y):
        self.x = x
        self.y = y
        self.deg = tk.IntVar()
        self.sub_label = tk.Label(finger_window)
        self.sub_spinbox = tk.Spinbox(finger_window)
        self.sub_scale = tk.Scale(finger_window)

        # --------- activate function --------
        self.Label()
        self.Spinbox()
        self.Scale()

    def Label(self, fix_x=0, fix_y=0):
        self.sub_label.configure(text=self.label_text, font=('Times', 15, 'bold'))
        self.sub_label.place(x=self.x + fix_x, y=self.y + fix_y)

    def Spinbox(self):
        self.sub_spinbox.configure(from_=0, to=130, font=('Times', 15, 'bold'))
        self.sub_spinbox.configure(width=10)
        self.sub_spinbox.place(x=self.x, y=self.y + 40)
        self.sub_spinbox.configure(textvariable=self.deg)
        self.sub_spinbox.configure(command=self.Spinbox_function)

    def Scale(self):
        self.sub_scale.configure(from_=130, to=0, font=('Times', 15, 'bold'))
        self.sub_scale.configure(width=20, length=200)
        self.sub_scale.place(x=self.x, y=self.y + 80)
        self.sub_scale.configure(variable=self.deg)
        self.sub_scale.configure(bg='#FFFF00')
        self.sub_scale.configure(command=self.Scale_function)

    # -------- Function --------
    def Spinbox_function(self):
        spin_value = self.sub_spinbox.get()
        self.deg.set(spin_value)
        self.Change_Color(spin_value)
        # print('Spinbox:', self.label_text, spin_value)
        Serial.Transmit_value(self.transmit_port, spin_value)

    def Scale_function(self, v):
        scale_value = self.sub_scale.get()
        self.deg.set(scale_value)
        self.Change_Color(scale_value)
        # print('Scale:', self.label_text, scale_value)
        Serial.Transmit_value(self.transmit_port, scale_value)

    def Vision_function(self, input_value):
        # print('Vision:', input_value)
        self.sub_scale.set(input_value)
        self.deg.set(input_value)
        self.Change_Color(input_value)

    def Change_Color(self, input_value):
        color_number = str(hex(abs((130 - int(input_value)) * 25 // 13)))
        if len(color_number) < 4:
            color_number = '0' + color_number[2]
        else:
            color_number = color_number[2:]
        self.sub_scale.configure(bg='#FF' + color_number + '00')

    def Reset(self, text):
        if text == 'Arm':
            self.Vision_function(0)
        else:
            self.Vision_function(130)


class Main_GUI:
    def __init__(self):
        # -------- Variable --------
        self.main_window_x = 1530
        self.main_window_y = 540

        self.user_name = ''

        # -------- Object define --------
        self.main_window = None
        self.Close_button = None
        self.vision_canvas = None
        self.version_canvas = None
        self.Frame_Serial = None
        self.Frame_Serial_Canvas = None
        self.Frame_Login = None
        self.Frame_Login_Canvas = None
        self.Frame_Finger = None
        self.Frame_Finger_Canvas = None

        # -------- Run Program ---------
        self.GUI()
        '''Login.GUI()
        self.user_name = Login.user_index
        print('Main GUI', self.user_name)
        if not Login.cancel_flag:
            self.GUI()'''

    def GUI(self):
        # -------- GUI Initial --------
        self.main_window = tk.Tk()
        self.main_window.geometry(str(self.main_window_x) + 'x' + str(self.main_window_y))
        self.main_window.title('Hand Tracking GUI')
        self.main_window.resizable(width=False, height=False)

        # -------- Platform --------
        self.Close_button = tk.Button(self.main_window, text='Close', width=8,
                                      bg='#F93232', activebackground='#F93232',
                                      font=('Times', 14, 'bold'), command=self.close_window)
        self.Close_button.place(x=self.main_window_x - 160, y=self.main_window_y - 90)

        # -------- Vision Canvas --------
        self.vision_canvas = tk.Canvas(self.main_window, bg='black',
                                       width=640, height=480)
        self.vision_canvas.place(x=5, y=5)

        # -------- Version Canvas --------
        self.version_canvas = tk.Canvas(self.main_window, bg='#818286',
                                        width=1640, height=30)
        self.version_canvas.place(x=-2, y=self.main_window_y - 28)
        Version_label = tk.Label(self.main_window, text='Version 3.1  Made By Wade Tsai',
                                 font='Times 11 bold', bg='#818286')
        Version_label.place(x=1300, y=self.main_window_y - 25)

        # -------- The Frame of Serial --------
        self.Frame_Serial = tk.Frame(self.main_window, relief=tk.RAISED, borderwidth=3)
        self.Frame_Serial.place(x=650, y=5)
        self.Frame_Serial_Canvas = tk.Canvas(self.Frame_Serial, width=380, height=100)
        self.Frame_Serial_Canvas.pack()

        # -------- The Frame of Login System --------
        self.Frame_Login = tk.Frame(self.main_window, relief=tk.RAISED, borderwidth=3)
        self.Frame_Login.place(x=1310, y=5)
        self.Frame_Login_Canvas = tk.Canvas(self.Frame_Login, width=200, height=100)
        self.Frame_Login_Canvas.pack()

        # -------- The Frame of Finger action --------
        self.Frame_Finger = tk.Frame(self.main_window, relief=tk.RAISED, borderwidth=3)
        self.Frame_Finger.place(x=650, y=120)
        self.Frame_Finger_Canvas = tk.Canvas(self.Frame_Finger, width=860, height=290)
        self.Frame_Finger_Canvas.pack()

        # -------- Reset Button --------
        reset_button = tk.Button(self.main_window, text='Reset Motor', font=('Times', 15, 'bold'),
                                 width=10, command=self.reset)
        reset_button.place(x=660, y=430)

        # -------- Activate Function --------
        self.Activate_Serial_GUI()
        self.Activate_Finger_GUI()
        self.Activate_Vision_System()
        self.Activate_Logout()

        if Login.detect_flag or True:
            self.main_window.mainloop()

    def reset(self):
        Thumb.Reset(Thumb.label_text)
        Index_Finger.Reset(Index_Finger.label_text)
        Middle_Finger.Reset(Middle_Finger.label_text)
        Ring_Finger.Reset(Ring_Finger.label_text)
        Pinky.Reset(Pinky.label_text)
        Arm.Reset(Arm.label_text)
        Serial.Transmit_msg('K')

    def Logout_state(self):
        self.close_window()

        Login.GUI()
        self.user_name = Login.user_index
        print('Main GUI 2', self.user_name)
        if not Login.cancel_flag:
            self.GUI()

    def Create(self):
        self.close_window()
        Vision.stop_vision()
        Logout.Create_Account()
        self.GUI()

    def Delete(self):
        print(self.user_name)
        dlt_flag = tkinter.messagebox.askokcancel(title='Delete Account',
                                                  message='Do you want to DELETE?')
        if dlt_flag:
            MF.delete_data('Face Detection', self.user_name)
            os.remove('test_3/' + self.user_name + '.jpg')
            self.Logout_state()

    def Activate_Serial_GUI(self):
        Serial.GUI(self.main_window, 660, 15)

    def Activate_Finger_GUI(self):
        Thumb.GUI(self.main_window, 660, 125)
        Index_Finger.GUI(self.main_window, 795, 125)
        Middle_Finger.GUI(self.main_window, 930, 125)
        Ring_Finger.GUI(self.main_window, 1070, 125)
        Pinky.GUI(self.main_window, 1210, 125)
        Arm.GUI(self.main_window, 1380, 125)

        Thumb.Label(20)
        Pinky.Label(25)
        Arm.Label(25)

    def Activate_Vision_System(self):
        Vision.GUI(self.main_window)

    def Activate_Logout(self):
        Logout.GUI(self.main_window, 1325, 20)
        Logout.Logout_button.configure(command=self.Logout_state)
        Logout.Create_account_button.configure(command=self.Create)
        Logout.Delete_button.configure(command=self.Delete)

    def close_window(self):
        print('Close Window')
        Vision.stop_vision()
        self.main_window.destroy()
        Vision.camera.release()


b = time.time()
MF = My_Firebase()
FRC = Face_recognition()
Login = Login_System(1)

Serial = Serial_System()

Thumb = Finger_System('Thumb', 'A')
Index_Finger = Finger_System('Index_Finger', 'B')
Middle_Finger = Finger_System('Middle_Finger', 'C')
Ring_Finger = Finger_System('Ring_Finger', 'D')
Pinky = Finger_System('Pinky', 'E')
Arm = Finger_System('Arm', 'F')

Vision = Vision_System(1)
Logout = Logout_Create_System()

Main_GUI()
print(time.time() - b)
