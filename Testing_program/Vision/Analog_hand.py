from turtle import distance

import Tracking_model_v2 as TM2
import cv2
import math


class analog_hand(TM2.Media):
    def __init__(self, camera, mdc, mtc):
        super().__init__(camera, mdc, mtc)

    def normal(self):
        return super().tracking()

    def analog(self):
        my_list = self.my_dir
        t_image = super().tracking()

        if len(my_list) != 0:
            def finger_point(point, R_L):
                x, y, z = my_list[R_L][1][point][1], \
                          my_list[R_L][1][point][2], \
                          my_list[R_L][1][point][3]
                cv2.circle(t_image, (x, y), 12, (255, 0, 255), cv2.FILLED)
                return x, y, z

            x1 = y1 = z1 = x2 = y2 = z2 = 0
            if len(my_list) > 1:
                index_R = 0
                for kn in range(len(my_list)):
                    if my_list[kn][0] == 'Right':
                        index_R = kn
                x1, y1, z1 = finger_point(5, index_R)
                x2, y2, z2 = finger_point(8, index_R)
            else:
                if my_list[0][0] == 'Right':
                    x1, y1, z1 = finger_point(5, 0)
                    x2, y2, z2 = finger_point(8, 0)

            dist = math.sqrt((x1 - x2) ** 2 + (y1 - y2) ** 2)
            long = (z1 + z2) / 2 * 100

            a = math.sqrt(x1 ** 2 + (y1 - 480) ** 2)
            b = math.sqrt((x1 - 640) ** 2 + (y1 - 480) ** 2)
            af_1 = (a ** 2 + 640 ** 2 - b ** 2) / 2 * a * 640 / 170000000000
            bt_1 = (b ** 2 + 640 ** 2 - a ** 2) / 2 * b * 640 / 170000000000
            if -1.0 <= af_1 <= 1.0:
                AF = math.acos(af_1)
            else:
                AF = 0
            if -1.0 <= bt_1 <= 1.0:
                BT = math.acos(bt_1)
            else:
                BT = 0
            d = 640*(math.sin(AF) * math.sin(BT)) / math.sin(AF + BT)

            cv2.line(t_image, (x1, y1), (x2, y2), (255, 0, 255), 3)
            cv2.putText(t_image, str(int(dist)), (30, 50),
                        cv2.FONT_HERSHEY_COMPLEX, 0.5, (255, 0, 0), 1, cv2.LINE_AA)
            cv2.putText(t_image, str(int(long)), (30, 80),
                        cv2.FONT_HERSHEY_COMPLEX, 0.5, (255, 0, 0), 1, cv2.LINE_AA)
            cv2.putText(t_image, str(d), (30, 110),
                        cv2.FONT_HERSHEY_COMPLEX, 0.5, (255, 0, 0), 1, cv2.LINE_AA)

        return t_image


cam = cv2.VideoCapture(0)
track = analog_hand(cam, 0.6, 0.8)
while True:
    image = track.analog()
    cv2.imshow('hand', image)

    if cv2.waitKey(1) & 0xff == ord('q'):
        break

cam.release()
cv2.destroyAllWindows()
