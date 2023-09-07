import serial
import time
import keyboard

Serial_BaudRate = 38400
Serial_Port = 'COM4'

print('Connecting to device ...')
# ser = serial.Serial(Serial_Port, Serial_BaudRate, timeout=3)
ser = serial.Serial()
ser.baudrate = Serial_BaudRate
ser.port = Serial_Port

ser.open()
print('Connect successful')


def transform(data_in):
    if data_in >= 100:
        data_send = str(data_in)
    elif 100 > data_in >= 10:
        data_send = '0' + str(data_in)
    else:
        data_send = '00' + str(data_in)
    return data_send


while True:
    def key():
        if keyboard.is_pressed('q'):
            for i in range(0, 500):
                send_data = 'A' + transform(i) + '/'
                print(send_data)
                ser.write(send_data.encode('utf-8'))
                time.sleep(0.05)
        elif keyboard.is_pressed('w'):
            for i in range(0, 10):
                send_data = 'A' + str(i) + '/'
                print(send_data)
                ser.write(send_data.encode('utf-8'))
                time.sleep(0.2)
        elif keyboard.is_pressed(';'):
            send_data = 'A/'
            print(send_data)
            ser.write(send_data.encode('utf-8'))
            time.sleep(0.1)
        elif keyboard.is_pressed('s'):
            send_data = 'S/'
            print(send_data)
            ser.write(send_data.encode('utf-8'))
            time.sleep(0.5)
        elif keyboard.is_pressed('c'):
            send_data = 'C/'
            print(send_data)
            ser.write(send_data.encode('utf-8'))
            time.sleep(0.5)

    '''print('Send Data: A/')
    ser.write('A/'.encode('utf-8'))


    #print(ser.readline())
    time.sleep(0.5)
    print('Send Data: B/')
    ser.write('B/'.encode('utf-8'))
    time.sleep(0.5)
    # print(ser.readline())
    print('over')'''

    for i in range(0, 500):
        send_data = 'A' + transform(i) + '/'
        print(send_data)
        ser.write(send_data.encode('utf-8'))
        time.sleep(0.05)
