import tkinter as tk
from tkinter import ttk
import time as t
import cv2
import serial.tools.list_ports
from PIL import ImageTk, Image
from Track_package import Tracking_model_v2 as tm2


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
class Serial_GUI:
    def __init__(self, window, x, y):
        # -------- Variable define --------
        self.Serial_BaudRate = 38400
        self.ser = serial.Serial()
        self.list_of_port = []
        self.x = x
        self.y = y

        # -------- Scan Serial Port --------
        self.Scan_Serial_Port()

        # -------- Object define --------
        self.label = tk.Label(window, text='Select Serial Port:', font=('Times', 16, 'bold'))
        self.label.place(x=self.x, y=self.y)

        self.combobox = ttk.Combobox(window, value=self.list_of_port,
                                     font=('Times', 14, 'bold'))
        self.combobox.place(x=self.x, y=self.y + 30)

        self.Connect_button = tk.Button(window, text='Connect', width=10,
                                        font=('Times', 14, 'bold'),
                                        command=self.Connect_Serial_Port)
        self.Connect_button.place(x=self.x + 240, y=self.y)

        self.Disconnect_button = tk.Button(window, text='Disconnect', width=10,
                                           font=('Times', 14, 'bold'),
                                           command=self.Disconnect_Serial_Port)
        self.Disconnect_button.place(x=self.x + 240, y=self.y + 50)

    def Scan_Serial_Port(self):
        list_ports = serial.tools.list_ports.comports()
        print('Scan')
        for port in list_ports:
            self.list_of_port.append(port.name)
            print(port.name)

    def Connect_Serial_Port(self):
        print('Connecting to device')
        try:
            self.ser.baudrate = self.Serial_BaudRate
            self.ser.port = self.combobox.get()
            self.ser.open()
        except EnvironmentError:
            print('Connect Fail !!!!')

    def Disconnect_Serial_Port(self):
        print('Disconnect Serial Port')
        self.ser.close()

    def Transmit(self, port, value):
        send_data = port + Data_Transform(value) + '/'
        print(send_data)
        self.ser.write(send_data.encode('utf-8'))
        t.sleep(0.015)


class Login_system_GUI:
    def __init__(self, window, x, y):
        # ----- Variable -----
        self.x = x
        self.y = y
        self.in_out = True
        # ----- Form -----
        self.Login_out_button = tk.Button(window, text='Login', width=7,
                                          font=('Times', 13, 'bold'), command=self.logout)
        self.Login_out_button.place(x=self.x + 100, y=self.y)

        self.Create_account_button = tk.Button(window, text='Create', width=7,
                                               font=('Times', 13, 'bold'))
        self.Create_account_button.place(x=self.x, y=self.y)

        self.Delete_button = tk.Button(window, text='Delete', width=7,
                                       font=('Times', 13, 'bold'), state=tk.DISABLED)
        self.Delete_button.place(x=self.x + 100, y=self.y + 40)

    def logout(self):
        if self.in_out:
            self.Login_out_button.configure(text='Logout')
            self.Delete_button.configure(state=tk.NORMAL)
            self.in_out = False
        else:
            self.Login_out_button.configure(text='Login')
            self.Delete_button.configure(state=tk.DISABLED)
            self.in_out = True


class Finger_GUI:
    def __init__(self, finger_window, x, y, text):
        # -------- Variable define --------
        self.x = x
        self.y = y
        self.label_text = text
        self.deg = tk.IntVar()
        self.deg.set(0)

        # -------- Object define --------
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

    def Scale(self):
        self.sub_scale.configure(from_=130, to=0, font=('Times', 15, 'bold'))
        self.sub_scale.configure(width=20, length=200)
        self.sub_scale.place(x=self.x, y=self.y + 80)
        self.sub_scale.configure(variable=self.deg)
        self.sub_scale.configure(bg='#FFFF00')


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
        Version_label = tk.Label(self.main_window, text='Version 3.0  Made By Wade Tsai',
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

        # -------- Activate Function --------
        self.Activate_Serial_GUI()
        self.Activate_Finger_GUI()
        self.Activate_Login_GUI()

        self.main_window.mainloop()

    def Activate_Finger_GUI(self):
        Thumb = Finger_GUI(self.main_window, 660, 125, 'Thumb')
        Index_Finger = Finger_GUI(self.main_window, 795, 125, 'Index Finger')
        Middle_Finger = Finger_GUI(self.main_window, 930, 125, 'Middle_Finger')
        Ring_Finger = Finger_GUI(self.main_window, 1070, 125, 'Ring_Finger')
        Pinky = Finger_GUI(self.main_window, 1210, 125, 'Pinky')
        Arm = Finger_GUI(self.main_window, 1380, 125, 'Arm')

        Thumb.Label(20)
        Pinky.Label(25)
        Arm.Label(25)

    def Activate_Serial_GUI(self):
        Serial_GUI(self.main_window, 660, 15)

    def Activate_Login_GUI(self):
        Login_system_GUI(self.main_window, 1325, 20)

    def close_window(self):
        print('Close Window')
        self.main_window.destroy()


Main_GUI()
