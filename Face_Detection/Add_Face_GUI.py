import tkinter as tk
from tkinter import filedialog as fd
import cv2
from PIL import ImageTk, Image

window = tk.Tk()
window.geometry('780x485')
window.title('Add New Face')

file_path = tk.StringVar()
file_path.set(' ')


# ----------------- Program ---------------
class Video_Cam:
    def __init__(self):
        self.camera = cv2.VideoCapture(0)
        cam_width = self.camera.get(cv2.CAP_PROP_FRAME_WIDTH)
        cam_height = self.camera.get(cv2.CAP_PROP_FRAME_HEIGHT)
        ret, self.image = self.camera.read()
        self.image_F = Image.fromarray(self.image)
        self.image_tk = ImageTk.PhotoImage(image=self.image_F)
        self.canvas = tk.Canvas(window, width=cam_width, height=cam_height, bg='black')
        self.canvas.place(x=1, y=1)
        self.img_canvas = self.canvas.create_image(cam_width/2+2, cam_height/2+2, image=self.image_tk)
        self.canvas.after(1, self.refresh_cam)

    def refresh_cam(self):
        ret, self.image = self.camera.read()
        image = cv2.flip(self.image, 1)
        image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        self.image_F = Image.fromarray(image)
        self.image_tk = ImageTk.PhotoImage(image=self.image_F)
        self.canvas.itemconfig(self.img_canvas, image=self.image_tk)
        self.canvas.after(1, self.refresh_cam)

    def cap(self):
        save_img = self.image
        file_name = fd.asksaveasfile(initialfile='Sample.jpg', defaultextension='.jpg',
                                     filetypes=[('All Files', '*.*')])
        cv2.imwrite(file_name.name, save_img)
        print(file_name.name)
        print('Save')


def Close():
    print('Close GUI')
    window.destroy()


c = Video_Cam()
# ----------------- Platform --------------
Close_button = tk.Button(window, text='Close', width=8,
                         bg='#F93232', activebackground='#F93232',
                         font=('Times', 14, 'bold'), command=Close)
Close_button.place(x=650, y=420)

Add_button = tk.Button(window, text='Capture', width=8, height=4,
                       bg='#00FF46', activebackground='#00FF46',
                       font=('Times', 16, 'bold'), command=c.cap)
Add_button.place(x=650, y=100)


window.mainloop()
