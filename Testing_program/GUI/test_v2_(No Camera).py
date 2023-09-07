import tkinter as tk
"""
    asdasddasdjalldsjl
"""
# ------------- GUI Setup -----------------
window = tk.Tk()
window.geometry('960x480')
window.title('Hand Tracking GUI')


# ------------- Program -------------------
class label_A:
    def __init__(self):
        self.second = 0
        self.label = tk.Label(window, text='0 s', font=('Times', 20))
        self.label.place(x=750, y=400)
        self.label.after(1000, self.refresh)

    def refresh(self):
        self.second += 1
        self.label.configure(text="%i s" % self.second)
        self.label.after(1000, self.refresh)


def Close():
    print('Close GUI')
    window.destroy()


# ------------- Platform Setting ----------

Close_button = tk.Button(window, text='Close', width=8, font=('Times', 14, 'bold'), command=Close)
Close_button.place(x=800, y=400)

dd = label_A()

window.mainloop()
