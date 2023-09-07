import tkinter as tk
import time as t
import math
import cv2
import serial
from PIL import ImageTk, Image
from Track_package import Tracking_model_v2 as tm2

# ---------------- Serial Setup -----------------------------
Serial_BaudRate = 9600
Serial_Port = 'COM4'

print('Connecting to device ...')
try:
    ser = serial.Serial(Serial_Port, Serial_BaudRate, timeout=3)
    print('Connect successful')
except EnvironmentError:
    print('Connect Fail !!!!')

# ------------- GUI Setup -----------------
window = tk.Tk()
window_x = 1530
window_y = 540
window.geometry(str(window_x) + 'x' + str(window_y))
window.title('Hand Tracking GUI')


# ------------- Program -------------------
class Running_time:
    def __init__(self):
        self.second = 0
        self.label = tk.Label(window, text='0 s', font=('Times', 10))
        self.label.place(x=window_x - 160, y=window_y - 130)
        self.label.after(1000, self.refresh)

    def refresh(self):
        self.second += 1
        self.label.configure(text="%i s" % self.second)
        self.label.after(1000, self.refresh)


class Vision:
    def __init__(self):
        cam_width = camera.get(cv2.CAP_PROP_FRAME_WIDTH)
        cam_height = camera.get(cv2.CAP_PROP_FRAME_HEIGHT)
        self.pTime = 0
        ret, image = camera.read()
        self.image_F = Image.fromarray(image)
        self.image_tk = ImageTk.PhotoImage(image=self.image_F)
        self.canvas = tk.Canvas(window, width=cam_width, height=cam_height, bg='black')
        self.canvas.place(x=5, y=5)
        self.img_canvas = self.canvas.create_image(cam_width / 2 + 2, cam_height / 2 + 2,
                                                   image=self.image_tk)
        self.canvas.after(1, self.re_can)

    def re_can(self):
        image = recognize.digital_finger()
        image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
        self.image_F = Image.fromarray(image)
        self.image_tk = ImageTk.PhotoImage(image=self.image_F)
        self.canvas.itemconfig(self.img_canvas, image=self.image_tk)
        self.canvas.after(1, self.re_can)


class Hand_Tracking(tm2.Media):
    def __init__(self, cam, mdc, mtc):
        super().__init__(cam, mdc, mtc)
        self.flag = {'Right': False,
                     'Left': False,
                     'Middle': True}
        self.Num = {'Right': None,
                    'Left': None}

    def nor_tracking(self):
        return super().tracking()

    def digital_finger(self):
        image = super().tracking()
        my_list = self.my_dir

        if len(my_list) != 0:
            def cir(point, rl):
                x, y = my_list[rl][1][point][1], my_list[rl][1][point][2]
                cv2.circle(image, (x, y), 13, (255, 0, 255), cv2.FILLED)
                return x, y

            def Finger_up_down(RL_index):
                def rec(index):
                    L = []
                    st = []
                    for asd in range(1, 11):
                        x, y = cir(asd * 2, index)
                        L.append([x, y])
                    st.append(abs(L[0][0]) - abs(L[1][0]))
                    for k in range(2, 9, 2):
                        st.append(abs(L[k][1]) - abs(L[k + 1][1]))
                    return st

                pt = rec(RL_index)
                ps = ''
                func_list = [Thumb,
                             Index_Finger,
                             Middle_Finger,
                             Ring_Finger,
                             Pinky]
                Value_text.delete('1.0', 'end')
                for i, class_name in enumerate(func_list):
                    ps += 'Finger ' + str(i + 1)
                    if pt[i] > 5:
                        class_name.print_set(130)
                        ps += ' up'
                    elif pt[i] < -5:
                        class_name.print_set(0)
                        ps += ' down'
                    ps += '\n'
                Value_text.insert('1.0', ps)

            def Arm_up_down(index):
                x, y = cir(9, index)
                if 138 <= abs(y) <= 380:
                    Arm.print_set(100 - int((380 - abs(y)) * (10 / 24)))

            def Arm_R_L(index):
                x, y = cir(9, index)
                if 100 <= abs(x) <= 500:
                    Wrist.print_set(int((300 - abs(x)) * (13 / 40)))

            def Slide(index):
                cv2.line(image, (150, 0), (150, 480), (255, 0, 0), 2)
                cv2.line(image, (490, 0), (490, 480), (255, 0, 0), 2)

                if len(my_list) != 0 and my_list[0][0] == 'Right':
                    px, py = cir(9, index)
                    if 150 < px < 490:
                        if not self.flag['Middle']:
                            self.flag['Middle'] = True
                            print('Middle')
                            send_data = 'S/'
                            ser.write(send_data.encode('utf-8'))
                    else:
                        if self.flag['Middle']:
                            self.flag['Middle'] = False

                    if px > 490:
                        if not self.flag['Right']:
                            self.flag['Right'] = True
                            print('Right')
                            send_data = 'F/'
                            ser.write(send_data.encode('utf-8'))

                        speed = (px - 490) // 10
                        if self.Num['Right'] != speed:
                            if 13 - speed < 0:
                                speed = 11
                            final_speed = (13 - speed) * 100 + 300
                            print(speed, final_speed)
                            value_data = 'A' + transform(final_speed) + '/'
                            ser.write(value_data.encode('utf-8'))
                            self.Num['Right'] = speed
                    else:
                        if self.flag['Right']:
                            self.flag['Right'] = False

                    if px < 150:
                        if not self.flag['Left']:
                            self.flag['Left'] = True
                            print('Left')
                            send_data = 'B/'
                            ser.write(send_data.encode('utf-8'))
                        speed = (150 - px) // 10
                        if self.Num['Left'] != speed:
                            if 13 - speed < 0:
                                speed = 11
                            final_speed = (13 - speed) * 100 + 300
                            print(speed, final_speed)
                            value_data = 'A' + transform(final_speed) + '/'
                            ser.write(value_data.encode('utf-8'))
                            self.Num['Left'] = speed
                    else:
                        if self.flag['Left']:
                            self.flag['Left'] = False

            if len(my_list) > 1:
                index_R = 0
                for kn in range(len(my_list)):
                    if my_list[kn][0] == 'Right':
                        index_R = kn
                Finger_up_down(index_R)
                Arm_up_down(index_R)
                Arm_R_L(index_R)
            else:
                if my_list[0][0] == 'Right':
                    Finger_up_down(0)
                    Arm_up_down(0)
                    Arm_R_L(0)

        return image

    def analog(self):
        my_list = self.my_dir
        t_image = super().tracking()

        if len(my_list) != 0 and my_list[0][0] == 'Right':

            def finger_point(point, R_L):
                x, y = my_list[R_L][1][point][1], \
                       my_list[R_L][1][point][2]
                # cv2.circle(t_image, (x, y), 12, (255, 0, 255), cv2.FILLED)
                return x, y

            def distance(point_1, point_2, R_L):
                x1, y1 = finger_point(point_1, R_L)
                x2, y2 = finger_point(point_2, R_L)
                dist = math.sqrt((x1 - x2) ** 2 + (y1 - y2) ** 2)
                return dist

            def distance_scale(point_1, point_2, sc, R_L=0):
                origin_dist = distance(0, point_1, R_L)
                dist = distance(point_1, point_2, R_L)
                return dist / origin_dist * sc

            Thumb_Scale = distance_scale(2, 4, 160)
            Index_Scale = distance_scale(5, 8, 163)
            Middle_Scale = distance_scale(9, 12, 145)
            Ring_Scale = distance_scale(13, 16, 160)
            Pinky_Scale = distance_scale(17, 20, 160)

            test_scale = [Thumb_Scale, Index_Scale, Middle_Scale, Ring_Scale, Pinky_Scale]
            if Thumb_Scale > 130:
                Thumb_Scale = 130
            if Index_Scale > 130:
                Index_Scale = 130
            if Middle_Scale > 130:
                Middle_Scale = 130
            if Ring_Scale > 130:
                Ring_Scale = 130
            if Pinky_Scale > 130:
                Pinky_Scale = 130

            Thumb.print_set(int(Thumb_Scale))
            Index_Finger.print_set(int(Index_Scale))
            Middle_Finger.print_set(int(Middle_Scale))
            Ring_Finger.print_set(int(Ring_Scale))
            Pinky.print_set((int(Pinky_Scale)))

        return t_image


class GUI_module:
    def __init__(self, x, y, text):
        self.x = x
        self.y = y
        self.text = text
        self.deg = tk.IntVar()
        self.deg.set(0)
        self.Label = tk.Label(window)
        self.Spinbox = tk.Spinbox(window)
        self.Scale = tk.Scale(window)
        self.label()
        self.spinbox()
        self.scale()

    def label(self, sx=0, sy=0):
        self.Label.configure(text=self.text, font='Times 15 bold')
        self.Label.place(x=self.x + sx, y=self.y + sy)

    def spinbox(self):
        self.Spinbox.configure(from_=0, to=130, font='Times 15 bold')
        self.Spinbox.configure(width=10)
        self.Spinbox.place(x=self.x, y=self.y + 40)
        self.Spinbox.configure(textvariable=self.deg)
        self.Spinbox.configure(command=self.Spinbox_function)

    def scale(self):
        self.Scale.configure(from_=130, to=0, font='Times 15 bold')
        self.Scale.configure(width=20, length=200)
        self.Scale.place(x=self.x, y=self.y + 80)
        self.Scale.configure(variable=self.deg)
        self.Scale.configure(bg='#FFFF00')
        self.Scale.configure(command=self.Scale_function)

    def Scale_function(self, fg):
        value = self.Scale.get()
        self.deg.set(value)
        transport(self.text, value)
        self.clo(value)

    def Spinbox_function(self):
        value = self.Spinbox.get()
        self.deg.set(value)
        transport(self.text, value)
        self.clo(value)

    def print_set(self, num):
        self.Scale.set(num)
        self.Spinbox.configure(value=str(num))
        self.clo(num)

    def clo(self, mm):
        nnn = str(hex(abs((130 - mm) * 25 // 13)))
        if len(nnn) < 4:
            kk = '0' + nnn[2]
        else:
            kk = nnn[2:]
        self.Scale.configure(bg='#FF' + kk + '00')


class Horizon_module(GUI_module):
    def __init__(self, x, y, text):
        super().__init__(x, y, text)

    def label(self, sx=0, sy=0):
        super().label()
        self.Label.place(x=self.x + sx, y=self.y + sy)

    def spinbox(self):
        super().spinbox()
        self.Spinbox.place(x=self.x + 40, y=self.y + 45)

    def scale(self):
        super().scale()
        self.Scale.configure(orient='horizontal')
        self.Scale.configure(from_=65, to=-65)

    def print_set(self, num):
        super().print_set(num)

    def clo(self, mm):
        nnn = str(hex(255 - int(abs((mm * 25 / 6.5)))))
        if len(nnn) < 4:
            kk = '0' + nnn[2]
        else:
            kk = nnn[2:]
        self.Scale.configure(bg='#FF' + kk + '00')


def transform(data_in):
    if data_in >= 100:
        data_send = str(data_in)
    elif 100 > data_in >= 10:
        data_send = '0' + str(data_in)
    else:
        data_send = '00' + str(data_in)
    return data_send


def transport(sl, value):
    data = ['Thumb', 'Index_Finger', 'Middle_Finger', 'Ring_Finger', 'Pinky', 'Arm']  # , 'Wrist']
    port = ['A', 'B', 'C', 'D', 'E', 'F', 'G']
    for num, name in enumerate(data):
        if sl == name:
            send_data = port[num] + transform(value) + '/'
            # print(send_data)
            ser.write(send_data.encode('utf-8'))
            t.sleep(0.005)


def Close():
    print('Close GUI')
    window.destroy()


# ------------- Platform Setting ----------
Close_button = tk.Button(window, text='Close', width=8,
                         bg='#F93232', activebackground='#F93232',
                         font=('Times', 14, 'bold'), command=Close)
Close_button.place(x=window_x - 160, y=window_y - 100)

Version_canvas = tk.Canvas(window, bg='#818286',
                           width=1640, height=30)
Version_canvas.place(x=-2, y=512)

Version_label = tk.Label(window, text='Version 1.8  Made By Wade Tsai',
                         font='Times 11 bold', bg='#818286')
Version_label.place(x=1300, y=515)

Value_text = tk.Text(window, width=20, height=5.5, font=('Times', 14, 'bold'))
Value_text.place(x=670, y=350)

canvas = tk.Canvas(window, width=640, height=480, bg='black')
canvas.place(x=5, y=5)

# combo = ttk.Combobox(window, font='Times', width=15, height=5, value=serial_ports())
# combo.place(x=1170, y=350)

# ------------- Class setup -------------
camera = cv2.VideoCapture(1)
run_time = Running_time()
recognize = Hand_Tracking(camera, 0.5, 0.8)
camera = Vision()

# ------------- Parameters setup ---------
Thumb = GUI_module(650, 25, 'Thumb')
Index_Finger = GUI_module(790, 25, 'Index_Finger')
Middle_Finger = GUI_module(930, 25, 'Middle_Finger')
Ring_Finger = GUI_module(1070, 25, 'Ring_Finger')
Pinky = GUI_module(1210, 25, 'Pinky')
Arm = GUI_module(1350, 25, 'Arm')
Wrist = Horizon_module(940, 350, 'Wrist')

Thumb.label(20)
Pinky.label(25)
Arm.label(25)
Wrist.label(35)

window.mainloop()
portc = ['A', 'B', 'C', 'D', 'E', 'F', 'G']
'''for name in portc:
    send_data = name + transform(120) + '/'
    print(send_data)
    ser.write(send_data.encode('utf-8'))
    t.sleep(0.01)'''
