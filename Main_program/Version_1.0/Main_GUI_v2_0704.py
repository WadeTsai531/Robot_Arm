import tkinter as tk
import cv2
import math
import time
from PIL import ImageTk, Image
import Tracking_model_v1 as tm1


# ------------- GUI Setup -----------------
window = tk.Tk()
window.geometry('1640x540')
window.title('Hand Tracking GUI')


# ------------- Program -------------------
class Running_time:
    def __init__(self):
        self.second = 0
        self.label = tk.Label(window, text='0 s', font=('Times', 10))
        self.label.place(x=1480, y=500)
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


class Hand_Tracking(tm1.Media):
    def __init__(self, cam, mdc, mtc):
        super().__init__(cam, mdc, mtc)

    def nor_tracking(self):
        return super().tracking()

    def digital_finger(self):
        image = super().tracking()
        my_list = self.my_list

        if len(my_list) != 0:
            def cir(point):
                x, y = my_list[point][1], my_list[point][2]
                cv2.circle(image, (x, y), 13, (255, 0, 255), cv2.FILLED)
                return x, y

            def line(point1, point2, color):
                x1, y1 = cir(point1)
                x2, y2 = cir(point2)
                cv2.circle(image, (x2, y2), 13, (255, 0, 255), cv2.FILLED)
                cv2.line(image, (x1, y1), (x2, y2), color, 3)

                point_x = x1 - x2
                point_y = y1 - y2

                d = math.sqrt(point_x ** 2 + point_y ** 2)

                cv2.putText(image, str(int(d)),
                            (x1 - point_x // 2, y1 - point_y // 2),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.5, color, 1, cv2.LINE_AA)
                return d

            def rec():
                L = []
                st = []
                for i in range(1, 11):
                    x, y = cir(i * 2)
                    L.append([x, y])
                cv2.putText(image, 'fig_1 = ' + str(L[0][0] - L[1][0]), (30, 50),
                            cv2.FONT_HERSHEY_SIMPLEX,
                            0.5, (255, 0, 255), 1, cv2.LINE_AA)
                st.append(abs(L[0][0]) - abs(L[1][0]))
                for k in range(2, 9, 2):
                    st.append(abs(L[k][1]) - abs(L[k+1][1]))
                    cv2.putText(image, 'fig ' + str(k//2+1)+' = '+str(st), (30, 60 + k*10),
                                cv2.FONT_HERSHEY_SIMPLEX,
                                0.5, (255, 0, 255), 1, cv2.LINE_AA)
                return st

            pt = rec()
            if pt[0] > 0:
                Fig_1.print_set(130)
                cv2.putText(image, 'Finger 1 up', (30, 170),
                            cv2.FONT_HERSHEY_SIMPLEX,
                            0.5, (255, 0, 255), 1, cv2.LINE_AA)
            else:
                Fig_1.print_set(0)

            if pt[1] > 0:
                Fig_2.print_set(130)
                cv2.putText(image, 'Finger 2 up', (30, 190),
                            cv2.FONT_HERSHEY_SIMPLEX,
                            0.5, (255, 0, 255), 1, cv2.LINE_AA)
            else:
                Fig_2.print_set(0)

            if pt[2] > 0:
                Fig_3.print_set(130)
                cv2.putText(image, 'Finger 3 up', (30, 210),
                            cv2.FONT_HERSHEY_SIMPLEX,
                            0.5, (255, 0, 255), 1, cv2.LINE_AA)
            else:
                Fig_3.print_set(0)

            if pt[3] > 0:
                Fig_4.print_set(130)
                cv2.putText(image, 'Finger 4 up', (30, 230),
                            cv2.FONT_HERSHEY_SIMPLEX,
                            0.5, (255, 0, 255), 1, cv2.LINE_AA)
            else:
                Fig_4.print_set(0)

            if pt[4] > 0:
                Fig_5.print_set(130)
                cv2.putText(image, 'Finger 5 up', (30, 250),
                            cv2.FONT_HERSHEY_SIMPLEX,
                            0.5, (255, 0, 255), 1, cv2.LINE_AA)
            else:
                Fig_5.print_set(0)
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

    def label(self):
        self.Label.configure(text=self.text, font='Times 15 bold')
        self.Label.place(x=self.x, y=self.y)

    def spinbox(self):
        self.Spin.configure(from_=0, to=130, font='Times 15 bold')
        self.Spin.configure(width=10)
        self.Spin.place(x=self.x, y=self.y + 40)

    def scale(self):
        self.Scale.configure(from_=0, to=130, font='Times 15 bold')
        self.Scale.configure(width=20, length=200)
        self.Scale.place(x=self.x, y=self.y + 80)

    def print_set(self, num):
        self.Scale.set(num)
        self.Spin.configure(value=str(num))


def Close():
    print('Close GUI')
    window.destroy()


# ------------- Platform Setting ----------
Close_button = tk.Button(window, text='Close', width=8,
                         font=('Times', 14, 'bold'), command=Close)
Close_button.place(x=1480, y=460)

Value_text = tk.Text(window, width=40, height=5, font=('Times', 14, 'bold'))
Value_text.place(x=670, y=370)

canvas = tk.Canvas(window, width=640, height=480, bg='black')
canvas.place(x=5, y=5)

camera = cv2.VideoCapture(0)
cam_width = camera.get(cv2.CAP_PROP_FRAME_WIDTH)
cam_height = camera.get(cv2.CAP_PROP_FRAME_HEIGHT)

# ------------- Class setup -------------
run_time = Running_time()
recognize = Hand_Tracking(camera, 0.7, 0.7)
camera_on = Vision()

# ------------- Parameters setup ---------
fig_1_scale = tk.IntVar()
fig_1_scale.set(100)
Fig_1 = GUI_module(660, 25, 'Fig 1')
Fig_2 = GUI_module(800, 25, 'Fig 2')
Fig_3 = GUI_module(940, 25, 'Fig 3')
Fig_4 = GUI_module(1080, 25, 'Fig 4')
Fig_5 = GUI_module(1220, 25, 'Fig 5')

window.mainloop()
