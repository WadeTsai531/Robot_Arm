import tkinter as tk
from tkinter import ttk
import time as t
import cv2
import serial.tools.list_ports
from PIL import ImageTk, Image
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
        self.Serial_BaudRate = 38400
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
        self.serial_open = True
        try:
            self.ser.baudrate = self.Serial_BaudRate
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
        print('Serial Value:', send_data)
        # self.ser.write(send_data.encode('utf-8'))
        t.sleep(0.005)

    def Transmit_msg(self, port):
        send_data = port + '/'
        print('Serial Msg:', send_data)
        # self.ser.write(send_data.encode('utf-8'))


class Login_System:
    def __init__(self):
        # ----- Variable -----
        self.in_out = True

        # ----- Object define -----
        self.Login_out_button = None
        self.Create_account_button = None
        self.Delete_button = None

    def GUI(self, window, x, y):
        self.Login_out_button = tk.Button(window, text='Login', width=7,
                                          font=('Times', 13, 'bold'), command=self.logout)
        self.Login_out_button.place(x=x + 100, y=y)

        self.Create_account_button = tk.Button(window, text='Create', width=7,
                                               font=('Times', 13, 'bold'))
        self.Create_account_button.place(x=x, y=y)

        self.Delete_button = tk.Button(window, text='Delete', width=7,
                                       font=('Times', 13, 'bold'), state=tk.DISABLED)
        self.Delete_button.place(x=x + 100, y=y + 40)

    def logout(self):
        if self.in_out:
            self.Login_out_button.configure(text='Logout')
            self.Delete_button.configure(state=tk.NORMAL)
            self.in_out = False
        else:
            self.Login_out_button.configure(text='Login')
            self.Delete_button.configure(state=tk.DISABLED)
            self.in_out = True


class Vision_System:
    def __init__(self, cam_index):
        # ----- Variable -----
        self.canvas = None
        self.img_canvas = None
        self.image_tk = None
        self.Tracking_Enable = False
        self.Tracking_System = Hand_Tracking_System(0.6, 0.8)

        # ----- Camera -----
        self.camera = cv2.VideoCapture(cam_index)

    def GUI(self, window):
        ret, image = self.camera.read()
        image_F = Image.fromarray(image)
        self.image_tk = ImageTk.PhotoImage(image=image_F)
        cam_width = self.camera.get(cv2.CAP_PROP_FRAME_WIDTH)
        cam_height = self.camera.get(cv2.CAP_PROP_FRAME_HEIGHT)
        self.canvas = tk.Canvas(window, width=cam_width, height=cam_height, bg='black')
        self.canvas.place(x=5, y=5)
        self.img_canvas = self.canvas.create_image(cam_width / 2 + 2, cam_height / 2 + 2,
                                                   image=self.image_tk)
        self.canvas.after(1, self.vis_cam)

    def vis_cam(self):
        ret, image = self.camera.read()
        if self.Tracking_Enable:
            image = self.Tracking_System.digital_finger(image)
        else:
            image = self.Tracking_System.nor_tracking(image)
        image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
        image_F = Image.fromarray(image)
        self.image_tk = ImageTk.PhotoImage(image=image_F)
        self.canvas.itemconfig(self.img_canvas, image=self.image_tk)
        self.canvas.after(1, self.vis_cam)


class Hand_Tracking_System(Tracking_model_v3.Media):
    def __init__(self, mdc, mtc):
        super().__init__(mdc, mtc)
        self.flag = {'Right': False,
                     'Left': False,
                     'Middle': True}
        self.Num = {'Right': None,
                    'Left': None}

    def nor_tracking(self, image):
        return super().tracking(image)

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
            def cir(point, rl):
                x, y = my_list[rl][1][point][1], my_list[rl][1][point][2]
                cv2.circle(image, (x, y), 13, (255, 0, 255), cv2.FILLED)
                return x, y

            def Finger_up_down(RL_index):
                def distance(finger_index):
                    L = []
                    st = []
                    for finger_point in range(1, 11):
                        x, y = cir(finger_point * 2, finger_index)
                        L.append([x, y])
                    st.append(abs(L[0][0]) - abs(L[1][0]))
                    for k in range(2, 9, 2):
                        st.append(abs(L[k][1]) - abs(L[k + 1][1]))
                    return st
                finger_distance = distance(RL_index)
                for index, function_name in enumerate(finger_list[:5]):
                    if finger_distance[index] > 10:
                        function_name.Vision_function(130)
                    elif finger_distance[index] < -10:
                        function_name.Vision_function(0)

            def Arm_up_down(index):
                x, y = cir(9, index)
                if 138 <= abs(y) <= 380:
                    finger_list[5].Vision_function(110 - int((380 - abs(y)) * (11 / 24)))

            def Slide(index):
                px, py = cir(9, index)
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
                    Finger_up_down(index_R)
                    Arm_up_down(index_R)
                    Slide(index_R)

            else:
                if my_list[0][0] == 'Right':
                    Finger_up_down(0)
                    Arm_up_down(0)
                    Slide(0)

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
        print('Spinbox:', self.label_text, spin_value)
        Serial.Transmit_value(self.transmit_port, spin_value)

    def Scale_function(self, v):
        scale_value = self.sub_scale.get()
        self.deg.set(scale_value)
        self.Change_Color(scale_value)
        print('Scale:', self.label_text, scale_value)
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


class Main_GUI:
    def __init__(self):
        # -------- Variable --------
        self.main_window_x = 1530
        self.main_window_y = 540

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
        self.reset_button = tk.Button(self.main_window, text='Reset', font=('Times', 15, 'bold'),
                                      width=8, command=self.reset)
        self.reset_button.place(x=660, y=430)

        # -------- Activate Function --------
        b = t.time()
        self.Activate_Serial_GUI()
        self.Activate_Login_GUI()
        self.Activate_Finger_GUI()
        self.Activate_Vision_System()
        print(t.time() - b)

        self.main_window.mainloop()

    def reset(self):
        if Serial.serial_open:
            print('start tracking')
            Vision.Tracking_Enable = True
        else:
            Vision.Tracking_Enable = False

    def Activate_Serial_GUI(self):
        Serial.GUI(self.main_window, 660, 15)

    def Activate_Login_GUI(self):
        Login.GUI(self.main_window, 1325, 20)

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

    def close_window(self):
        print('Close Window')
        self.main_window.destroy()


Serial = Serial_System()
Login = Login_System()
Thumb = Finger_System('Thumb', 'A')
Index_Finger = Finger_System('Index_Finger', 'B')
Middle_Finger = Finger_System('Middle_Finger', 'C')
Ring_Finger = Finger_System('Ring_Finger', 'D')
Pinky = Finger_System('Pinky', 'E')
Arm = Finger_System('Arm', 'F')
Vision = Vision_System(0)

Main_GUI()
