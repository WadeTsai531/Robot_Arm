import time
import tkinter as tk


class label_A:
    def __init__(self):
        self.second = 0
        self.label = None
        self.run = None

    def GUI(self, window):
        self.label = tk.Label(window, text='0 s', font=('Times', 10))
        self.label.place(x=110, y=100)
        self.run = self.label.after(1000, self.refresh)

    def refresh(self):
        self.second += 1
        self.label.configure(text="%i s" % self.second)
        self.run = self.label.after(1000, self.refresh)

    def cancel(self):
        self.label.after_cancel(self.run)


class Main_GUI:
    def __init__(self):
        self.main_window = None
        self.button = None

        self.GUI()

    def GUI(self):
        self.main_window = tk.Tk()
        self.main_window.geometry('350x230')
        self.main_window.title('login')

        self.button = tk.Button(self.main_window, text='Praise', font=('Times', 16, 'bold'),
                                command=self.close)
        self.button.place(x=110, y=10)

        A.GUI(self.main_window)

        self.main_window.mainloop()

    def close(self):
        self.main_window.destroy()
        A.cancel()
        print('wait')
        time.sleep(1)
        self.GUI()


A = label_A()
Main_GUI()
