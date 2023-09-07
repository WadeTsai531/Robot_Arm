import tkinter as tk
import time as t
import serial

# ---------------- Serial Setup -----------------------------
Serial_BaudRate = 9600
Serial_Port = 'COM4'

print('Connecting to device ...')
ser = serial.Serial(Serial_Port, Serial_BaudRate, timeout=3)
print('Connect successful')

# --------------- GUI Setup ---------------------------------
window = tk.Tk()
window.title('Arm_GUI_v2')
window.geometry('480x320')

# --------------- Value Define ------------------------------
A_deg = tk.IntVar()
A_deg.set(0)


def transform(data_in):
    if data_in >= 100:
        data_send = str(data_in)
    elif 100 > data_in >= 10:
        data_send = '0' + str(data_in)
    else:
        data_send = '00' + str(data_in)
    return data_send


# ------------------ Function -------------------------------


def A_spin():
    A_value = A_spinbox.get()
    A_deg.set(A_value)
    data = 'A' + transform(int(A_value)) + '/'
    print(data)
    ser.write(data.encode('utf-8'))
    # ser.write(0b00101111)


def A_sl(A_c_value):
    A_c_value = A_scale.get()
    A_deg.set(A_c_value)
    data = 'A' + transform(int(A_c_value)) + '/'
    print(data)
    ser.write(data.encode('utf-8'))


def Close():
    print('close')
    window.destroy()


def send():
    sd = 'O/'
    print('Start motor')
    ser.write(sd.encode('utf-8'))


def stop():
    sd = 'S/'
    print('Stop motor')
    ser.write(sd.encode('utf-8'))


def RD():
    sd = 'F/'
    print('Dir: F')
    ser.write(sd.encode('utf-8'))


def LD():
    sd = 'B/'
    print('Dir: B')
    ser.write(sd.encode('utf-8'))


def CB():
    sd = 'C/'
    print('Cab')
    ser.write(sd.encode('utf-8'))


# ------------------ platform setup --------------------------
A_label = tk.Label(window, text='A motor', font=('Times', 18, 'bold'))
A_label.place(x=50, y=20)
A_spinbox = tk.Spinbox(window, from_=300, to=700, width=10, font=('Times', 18, 'bold'),
                       textvariable=A_deg, command=A_spin)
A_spinbox.place(x=50, y=60)
A_scale = tk.Scale(window, from_=300, to=700, width=20, length=200, font=('Times', 20, 'bold'),
                   variable=A_deg, command=A_sl)
A_scale.place(x=50, y=100)

Close_button = tk.Button(window, text='Close', font=('Times', 16, 'bold'), width=8, height=1, command=Close)
Close_button.place(x=350, y=190)

send_button = tk.Button(window, text='start', font=('Times', 16, 'bold'), width=8, height=1, command=send)
send_button.place(x=220, y=50)

stop_button = tk.Button(window, text='stop', font=('Times', 16, 'bold'), width=8, height=1, command=stop)
stop_button.place(x=220, y=120)

R_dir_button = tk.Button(window, text='Fow', font=('Times', 16, 'bold'), width=8, height=1, command=RD)
R_dir_button.place(x=350, y=50)

R_dir_button = tk.Button(window, text='Back', font=('Times', 16, 'bold'), width=8, height=1, command=LD)
R_dir_button.place(x=350, y=120)

CB_button = tk.Button(window, text='call', font=('Times', 16, 'bold'), width=8, height=1, command=CB)
CB_button.place(x=220, y=190)

# ------------------ platform setup end -----------------------
window.mainloop()
