import serial
import serial.tools.list_ports
import time
import keyboard

Serial_BaudRate = 19200
ser = serial.Serial()

list_of_comports = []
list_comports = serial.tools.list_ports.comports()
for comport in list_comports:
    list_of_comports.append(comport.name)
    print(comport.name)


def transform(data_in):
    if data_in >= 100:
        data_send = str(data_in)
    elif 100 > data_in >= 10:
        data_send = '0' + str(data_in)
    else:
        data_send = '00' + str(data_in)
    return data_send


ser.baudrate = 9600
ser.port = list_of_comports[0]
ser.open()

print('OK')

for i in range(5):
    ser.write('A/'.encode('utf-8'))
    print('A')
    time.sleep(1)
    ser.write('C/'.encode('utf-8'))
    print('C')
    time.sleep(1)

print('close')
ser.close()
