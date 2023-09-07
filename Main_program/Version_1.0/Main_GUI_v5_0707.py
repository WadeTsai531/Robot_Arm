import tkinter as tk
import cv2
from PIL import ImageTk, Image
import Tracking_model_v2 as tm2

# ------------- GUI Setup -----------------
window = tk.Tk()
window_x = 1640
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
                    if pt[i] > 10:
                        class_name.print_set(130)
                        ps += ' up'
                    elif pt[i] < -10:
                        class_name.print_set(0)
                        ps += ' down'
                    ps += '\n'
                Value_text.insert('1.0', ps)

            def Arm_up_down(index):
                x, y = cir(9, index)
                if 138 <= abs(y) <= 380:
                    Arm.print_set(int((380 - abs(y)) * (13 / 24)))

            def Arm_R_L(index):
                x, y = cir(9, index)
                if 100 <= abs(x) <= 500:
                    Wrist.print_set(int((300 - abs(x)) * (13 / 40)))

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


class GUI_module:
    def __init__(self, x, y, text):
        self.x = x
        self.y = y
        self.text = text
        self.Label = tk.Label(window)
        self.Spin = tk.Spinbox(window)
        self.Scale = tk.Scale(window)
        self.label()
        self.spinbox()
        self.scale()

    def label(self, sx=0, sy=0):
        self.Label.configure(text=self.text, font='Times 15 bold')
        self.Label.place(x=self.x + sx, y=self.y + sy)

    def spinbox(self):
        self.Spin.configure(from_=0, to=130, font='Times 15 bold')
        self.Spin.configure(width=10)
        self.Spin.place(x=self.x, y=self.y + 40)

    def scale(self):
        self.Scale.configure(from_=130, to=0, font='Times 15 bold')
        self.Scale.configure(width=20, length=200)
        self.Scale.place(x=self.x, y=self.y + 80)

    def print_set(self, num):
        self.Scale.set(num)
        self.Spin.configure(value=str(num))

        def clo(mm):
            nnn = str(hex(abs((130 - mm) * 25//13)))
            if len(nnn) < 4:
                kk = '0' + nnn[2]
            else:
                kk = nnn[2:]
            return kk
        self.Scale.configure(bg='#FF' + clo(num) + '00')


class Horizon_module(GUI_module):
    def __init__(self, x, y, text):
        super().__init__(x, y, text)

    def label(self, sx=0, sy=0):
        super().label()
        self.Label.place(x=self.x + sx, y=self.y + sy)

    def spinbox(self):
        super().spinbox()
        self.Spin.place(x=self.x + 40, y=self.y + 45)

    def scale(self):
        super().scale()
        self.Scale.configure(orient='horizontal')
        self.Scale.configure(from_=65, to=-65)

    def print_set(self, num):
        self.Scale.set(num)
        self.Spin.configure(value=str(num))

        def clo(mm):
            nnn = str(hex(255 - int(abs((mm * 25 / 6.5)))))
            if len(nnn) < 4:
                kk = '0' + nnn[2]
            else:
                kk = nnn[2:]
            return kk

        self.Scale.configure(bg='#FF' + clo(num) + '00')


def change():
    print(scale_1.get())
    print(scale_2.get())
    # version_canvas.configure(width=scale_1.get())


def Close():
    print('Close GUI')
    window.destroy()


# ------------- Platform Setting ----------
Close_button = tk.Button(window, text='Close', width=8,
                         bg='#F93232', activebackground='#F93232',
                         font=('Times', 14, 'bold'), command=Close)
Close_button.place(x=window_x - 160, y=window_y - 100)

s1 = tk.IntVar()
s2 = tk.IntVar()
scale_1 = tk.Spinbox(window, width=6, from_=0, to=window_x,
                     font='Times 14 bold', command=change)
scale_1.place(x=1200, y=400)

scale_2 = tk.Spinbox(window, width=6, from_=0, to=window_y,
                     font='Times 14 bold', command=change)
scale_2.place(x=1200, y=450)

Version_canvas = tk.Canvas(window, bg='#818286',
                           width=1640, height=30)
Version_canvas.place(x=-2, y=512)

Version_label = tk.Label(window, text='Version 1.5  Made By Wade Tsai',
                         font='Times 11 bold', bg='#818286')
Version_label.place(x=1400, y=515)

Value_text = tk.Text(window, width=20, height=5.5, font=('Times', 14, 'bold'))
Value_text.place(x=670, y=350)

canvas = tk.Canvas(window, width=640, height=480, bg='black')
canvas.place(x=5, y=5)

# ------------- Camera setup -----------------
camera = cv2.VideoCapture(0)
cam_width = camera.get(cv2.CAP_PROP_FRAME_WIDTH)
cam_height = camera.get(cv2.CAP_PROP_FRAME_HEIGHT)

# ------------- Class setup -------------

run_time = Running_time()
recognize = Hand_Tracking(camera, 0.6, 0.9)
camera_on = Vision()

# ------------- Parameters setup ---------
Thumb = GUI_module(670, 25, 'Thumb')
Thumb.label(20)
Index_Finger = GUI_module(820, 25, 'Index_Finger')
Middle_Finger = GUI_module(970, 25, 'Middle_Finger')
Ring_Finger = GUI_module(1120, 25, 'Ring_Finger')
Pinky = GUI_module(1270, 25, 'Pinky')
Pinky.label(25)
Arm = GUI_module(1420, 25, 'Arm')
Arm.label(25)
Wrist = Horizon_module(940, 350, 'Wrist Degree')
Wrist.label(35)

window.mainloop()
