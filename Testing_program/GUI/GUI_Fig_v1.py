import tkinter as tk
import cv2
import time
from PIL import ImageTk, Image

# ------------- GUI Setup -----------------
window = tk.Tk()
window.geometry('1280x540')
window.title('Hand Tracking GUI')


# ------------- Program -------------------
class label_A:
    def __init__(self):
        self.second = 0
        self.label = tk.Label(window, text='0 s', font=('Times', 10))
        self.label.place(x=1200, y=500)
        self.label.after(1000, self.refresh)

    def refresh(self):
        self.second += 1
        self.label.configure(text="%i s" % self.second)
        self.label.after(1000, self.refresh)


class video:
    def __init__(self):
        self.pTime = 0
        ret, image = camera.read()
        self.image_F = Image.fromarray(image)
        self.image_tk = ImageTk.PhotoImage(image=self.image_F)
        self.canvas = tk.Canvas(window, width=cam_width, height=cam_height, bg='black')
        self.canvas.place(x=5, y=5)
        self.img_canvas = self.canvas.create_image(cam_width/2+2, cam_height/2+2,
                                                   image=self.image_tk)
        self.canvas.after(1, self.re_can)

    def re_can(self):
        """cTime = time.time()
        fps = 1 / (cTime - self.pTime)
        self.pTime = cTime
        print(fps)"""
        ret, image = camera.read()
        image = cv2.flip(image, 1)
        image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        self.image_F = Image.fromarray(image)
        self.image_tk = ImageTk.PhotoImage(image=self.image_F)
        self.canvas.itemconfig(self.img_canvas, image=self.image_tk)
        self.canvas.after(1, self.re_can)


def Close():
    print('Close GUI')
    window.destroy()


# ------------- Platform Setting ----------
Close_button = tk.Button(window, text='Close', width=8,
                         font=('Times', 14, 'bold'), command=Close)
Close_button.place(x=1120, y=460)


class GUI_module:
    def __init__(self, x, y, text):
        self.tk = tk
        self.x = x
        self.y = y
        self.text = text
        self.label()
        self.spinbox()
        self.scale()

    def label(self):
        Label = self.tk.Label(window)
        Label.configure(text=self.text, font='Times 15 bold')
        Label.place(x=self.x, y=self.y)

    def spinbox(self):
        Spin = self.tk.Spinbox(window)
        Spin.configure(from_=0, to=130, font='Times 15 bold')
        Spin.configure(width=10)
        Spin.place(x=self.x, y=self.y + 40)

    def scale(self):
        Scale = self.tk.Scale(window)
        Scale.configure(from_=0, to=130, font='Times 15 bold')
        Scale.configure(width=20, length=200)
        Scale.place(x=self.x, y=self.y + 80)


Value_text = tk.Text(window, width=40, height=5, font=('Times', 14, 'bold'))
Value_text.place(x=650, y=370)
Value_text.insert("insert", "kkk")

canvas = tk.Canvas(window, width=640, height=480, bg='black')
canvas.place(x=5, y=5)

camera = cv2.VideoCapture(0)
cam_width = camera.get(cv2.CAP_PROP_FRAME_WIDTH)
cam_height = camera.get(cv2.CAP_PROP_FRAME_HEIGHT)
camera_on = video()

dd = label_A()
Fig_1 = GUI_module(660, 25, 'Fig 1')
Fig_2 = GUI_module(800, 25, 'Fig 2')
Fig_3 = GUI_module(940, 25, 'Fig 3')

window.mainloop()
