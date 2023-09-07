import tkinter as tk
import cv2
from PIL import ImageTk, Image


# ------------- GUI Setup -----------------
window = tk.Tk()
window.geometry('960x480')
window.title('Hand Tracking GUI')


# ------------- Program -------------------
def video_setup():
    can = tk.Canvas(window, bg='black', width=480, height=320)
    can.place(x=20, y=20)
    ret, image = camera.read()
    image_F = Image.fromarray(image)
    image_tk = ImageTk.PhotoImage(image=image_F)
    can.create_image(20, 20, image=image_tk)
    window.after(1, video())


def video():
    can = tk.Canvas(window, bg='black', width=480, height=320)
    can.place(x=20, y=20)
    ret, image = camera.read()
    image_F = Image.fromarray(image)
    image_tk = ImageTk.PhotoImage(image=image_F)
    can.create_image(20, 20, image=image_tk)
    window.after(1, video())


def Close():
    print('Close GUI')
    window.destroy()


# ------------- Platform Setting ----------

camera = cv2.VideoCapture('video_test1.mp4')

'''
image = cv2.imread('test.jpg')
image_F = Image.fromarray(image)
image_tk = ImageTk.PhotoImage(image=image_F)
image_label = tk.Label(window, image=image_tk)
image_label.place(x=50, y=50)
'''

Close_button = tk.Button(window, text='Close', width=8, font=('Times', 14, 'bold'), command=Close)
Close_button.place(x=800, y=400)

video_setup()
window.mainloop()
