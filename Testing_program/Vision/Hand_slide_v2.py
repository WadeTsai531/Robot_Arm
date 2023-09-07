from Track_package import Tracking_model_v2 as TM2
import cv2
import serial

# ---------------- Serial Setup -----------------------------
Serial_BaudRate = 9600
Serial_Port = 'COM4'

print('Connecting to device ...')
ser = serial.Serial(Serial_Port, Serial_BaudRate, timeout=3)
print('Connect successful')


class Hand_Track(TM2.Media):
    def __init__(self, camera):
        super().__init__(camera, 0.7, 0.6)
        self.flag = {'Right': False,
                     'Left': False,
                     'Middle': True}
        self.Num = {'Right': None,
                    'Left': None}

    def nor(self):
        return super().tracking()

    def slide(self):
        t_image = super().tracking()
        my_list = self.my_dir

        def cir(point):
            x, y = my_list[0][1][point][1], my_list[0][1][point][2]
            cv2.circle(t_image, (x, y), 10, (255, 0, 0), cv2.FILLED)
            return x, y

        def transform(data_in):
            if data_in >= 1000:
                data_send = str(data_in)
            elif 1000 > data_in >= 100:
                data_send = '0' + str(data_in)
            elif 100 > data_in >= 10:
                data_send = '00' + str(data_in)
            else:
                data_send = '000' + str(data_in)
            return data_send

        cv2.line(t_image, (150, 0), (150, 480), (255, 0, 0), 2)
        cv2.line(t_image, (490, 0), (490, 480), (255, 0, 0), 2)

        if len(my_list) != 0 and my_list[0][0] == 'Right':
            px, py = cir(9)
            if 150 < px < 490:
                if not self.flag['Middle']:
                    self.flag['Middle'] = True
                    print('Middle')
                    send_data = 'S/'
                    ser.write(send_data.encode('utf-8'))
            else:
                if self.flag['Middle']:
                    self.flag['Middle'] = False

            if px > 490:
                if not self.flag['Right']:
                    self.flag['Right'] = True
                    print('Right')
                    send_data = 'R/'
                    ser.write(send_data.encode('utf-8'))

                '''speed = (px - 490) // 10
                if self.Num['Right'] != speed:
                    if 13 - speed < 0:
                        speed = 11
                    final_speed = (13 - speed) * 100 + 300
                    print(speed, final_speed)
                    value_data = 'V' + transform(final_speed) + '/'
                    ser.write(value_data.encode('utf-8'))
                    self.Num['Right'] = speed'''
            else:
                if self.flag['Right']:
                    self.flag['Right'] = False

            if px < 150:
                if not self.flag['Left']:
                    self.flag['Left'] = True
                    print('Left')
                    send_data = 'L/'
                    ser.write(send_data.encode('utf-8'))

                '''speed = (150 - px) // 10
                if self.Num['Left'] != speed:
                    if 13 - speed < 0:
                        speed = 11
                    final_speed = (13 - speed) * 100 + 300
                    print(speed, final_speed)
                    value_data = 'V' + transform(final_speed) + '/'
                    ser.write(value_data.encode('utf-8'))
                    self.Num['Left'] = speed'''
            else:
                if self.flag['Left']:
                    self.flag['Left'] = False

        return t_image


cam = cv2.VideoCapture(1)
track = Hand_Track(cam)

while True:
    image = track.slide()
    cv2.imshow('Hand', image)

    if cv2.waitKey(1) & 0xff == ord('q'):
        break
cam.release()
cv2.destroyAllWindows()
