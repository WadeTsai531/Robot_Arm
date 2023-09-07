import time
import tkinter as tk
import cv2
import os
import numpy as np
import face_recognition
from PIL import ImageTk, Image

# --------- Tkinter ---------
window = tk.Tk()
window.geometry('860x485')
window.title('Delete Account')
window.resizable(width=False, height=False)

# --------- Form Design ---------
vision_canvas = tk.Canvas(window, width=640, height=480, bg='black')
vision_canvas.place(x=0, y=1)


# --------- Functions ---------
def close():
    print('Close GUI')
    window.destroy()


# --------- Camera ---------
class Video_Cam:
    def __init__(self):
        self.cap_flag = False
        self.cap_value = 0
        self.time_now = 0
        self.photo_name = ''

        self.camera = cv2.VideoCapture(0)
        cam_width = self.camera.get(cv2.CAP_PROP_FRAME_WIDTH)
        cam_height = self.camera.get(cv2.CAP_PROP_FRAME_HEIGHT)
        ret, self.image = self.camera.read()
        self.image_F = Image.fromarray(self.image)
        self.image_tk = ImageTk.PhotoImage(image=self.image_F)
        self.canvas = tk.Canvas(window, width=cam_width, height=cam_height, bg='black')
        self.canvas.place(x=1, y=1)
        self.img_canvas = self.canvas.create_image(cam_width / 2 + 2, cam_height / 2 + 2,
                                                   image=self.image_tk)
        self.canvas.after(1, self.refresh_cam)

    def refresh_cam(self):
        ret, self.image = self.camera.read()
        image = cv2.flip(self.image, 1)
        image = Fcr.Recognition(image)
        image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        # image = cv2.rectangle(image, (200, 100), (440, 380), (255, 0, 0), 3)

        if self.cap_value != 0:
            if self.cap_value == 1:
                self.time_now = time.time()
                self.cap_value = 2

            if int(time.time() - self.time_now) > 0:
                self.cap_value += 1
                self.time_now = time.time()

            if self.cap_value - 2 == 3 and not self.cap_flag:
                self.cap_flag = True
                self.Capture(self.photo_name)

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
        self.canvas.after(1, self.refresh_cam)

    def Capture(self, name):
        if self.cap_flag:
            save_img = self.image
            '''file_name = fd.asksaveasfile(initialfile='Sample.jpg', defaultextension='.jpg',
                                         filetypes=[('All Files', '*.*')])'''
            cv2.imwrite('pic/test_3/' + name + '.jpg', save_img)
            print(name + '.jpg')
            print('Save')
        else:
            self.photo_name = name
            self.cap_value = 1


# --------- Create New Account ---------
class Delete_Account:
    def __init__(self):
        # ------- Set Flag & Variable -------
        self.username = ''
        self.password = ''
        self.username_flag = False
        self.password_flag = False
        self.capture_flag = False

        # ------- Title -------
        self.label_0 = tk.Label(window, text='Delete Account',
                                font=('Times', 18, 'bold'))
        self.label_0.place(x=655, y=5)

        # -------- Username & Password -----------------
        password_y = 40
        self.frame = tk.Frame(window, relief=tk.RAISED, borderwidth=3)
        self.frame.place(x=645, y=password_y)

        self.canvas_1 = tk.Canvas(self.frame, width=200, height=150, bg='#E1E1E1')
        self.canvas_1.pack()

        self.label_1 = tk.Label(window, text='請輸入帳號名稱及密碼:', bg='#E1E1E1',
                                font=('microsoft yahei', 12, 'bold'))
        self.label_1.place(x=650, y=password_y + 5)

        self.label_2 = tk.Label(window, text='Username:', bg='#E1E1E1',
                                font=('Times', 16, 'bold'))
        self.label_2.place(x=650, y=password_y + 30)

        self.user_entry = tk.Entry(window, width=19,
                                   font=('Times', 12, 'bold'))
        self.user_entry.place(x=650, y=password_y + 60)

        self.label_3 = tk.Label(window, text='Password:', bg='#E1E1E1',
                                font=('Times', 16, 'bold'))
        self.label_3.place(x=650, y=password_y + 90)

        self.pass_entry = tk.Entry(window, width=19, show='*',
                                   font=('Times', 12, 'bold'))
        self.pass_entry.place(x=650, y=password_y + 120)

        # ----------- Capture --------------
        capture_y = 210
        self.frame_capture = tk.Frame(window, relief=tk.RAISED, borderwidth=3)
        self.frame_capture.place(x=645, y=capture_y)

        self.canvas_2 = tk.Canvas(self.frame_capture, width=200, height=110, bg='#E1E1E1')
        self.canvas_2.pack()

        self.label_c_1 = tk.Label(window, text='1. 將臉對準方格內\n'
                                               '2. 按下截圖按鈕',
                                  bg='#E1E1E1', justify=tk.LEFT,
                                  font=('microsoft yahei', 12, 'bold'))
        self.label_c_1.place(x=650, y=capture_y + 5)

        self.button_c_1 = tk.Button(window, text='Capture', width=15,
                                    font=('Times', 16, 'bold'),
                                    command=self.Cap, state=tk.DISABLED)
        self.button_c_1.place(x=655, y=capture_y + 60)

        # ----------- Create & Check --------------
        check_y = 340

        self.button_1 = tk.Button(window, text='Cancel', width=6,
                                  font=('Times', 14, 'bold'), command=close)
        self.button_1.place(x=650, y=440)

        self.button_2 = tk.Button(window, text='Register', width=6, state=tk.DISABLED,
                                  font=('Times', 14, 'bold'), command=self.register)
        self.button_2.place(x=780, y=440)

        self.Text_check = tk.Text(window, width=20, height=4,
                                  font=('Times', 14, 'bold'))
        self.Text_check.place(x=645, y=check_y)

        self.Text_check.insert('insert', 'Username:  \n')
        self.Text_check.insert('insert', 'Password:  \n')
        self.Text_check.insert('insert', 'Face Capture:  \n')

        self.Text_check.after(1, self.check)

    def Cap(self):
        Vision.Capture(self.user_entry.get())

    def check(self):
        if Vision.cap_flag:
            self.capture_flag = True

        if self.username_flag and self.password_flag and self.capture_flag:
            self.button_2.config(state=tk.NORMAL)

        if self.user_entry.get() != '' and len(self.user_entry.get()) > 3:  # Check username
            self.username_flag = True
            self.username = self.user_entry.get()
            self.button_c_1.config(state=tk.NORMAL)
            self.Text_check.delete('1.10', '1.17')
            self.Text_check.insert('1.10', 'OK!')

        if self.pass_entry.get() != '' and len(self.pass_entry.get()) > 7:  # Check password
            self.password_flag = True
            self.password = self.pass_entry.get()
            self.Text_check.delete('2.10', '2.17')
            self.Text_check.insert('2.10', 'OK!')

        if self.capture_flag:  # Check Capture
            self.Text_check.delete('3.14', '3.21')
            self.Text_check.insert('3.14', 'OK!')

        self.Text_check.after(1, self.check)

    def register(self):
        self.Text_check.insert('4.0', 'Upload Successful')
        print(self.username)
        print(self.password)
        print('OK')


# -------- Face Recognition --------
class Face_recognition:
    def __init__(self):
        # ----- Variable Define -----
        self.encode_list = []
        self.Name_list = []

        # ----- Encoding Picture -----
        self.Encoding_image()

    def Encoding_image(self):
        path = '../pic/test_3'
        for file in os.listdir(path):
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
                name = self.Name_list[match_index].upper()
                # print(name)
                y1, x2, y2, x1 = face_Loc
                y1, x2, y2, x1 = y1 * 4, x2 * 4, y2 * 4, x1 * 4
                cv2.rectangle(image, (x1, y1), (x2, y2), (0, 255, 0), 2)
                cv2.rectangle(image, (x1, y2 - 35), (x2, y2), (0, 255, 0), cv2.FILLED)
                cv2.putText(image, name, (x1 + 6, y2 - 6), cv2.FONT_HERSHEY_COMPLEX, 1,
                            (255, 255, 255), 2)

        return image


Fcr = Face_recognition()
Vision = Video_Cam()
Delete_Account()

window.mainloop()
