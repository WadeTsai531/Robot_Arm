from Track_package import Tracking_model_v2 as TM2
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

        if len(my_list) != 0 and my_list[0][0] == 'Right':
            def finger_point(point, R_L):
                x, y, z = my_list[R_L][1][point][1], \
                          my_list[R_L][1][point][2], \
                          my_list[R_L][1][point][3]
                cv2.circle(t_image, (x, y), 12, (255, 0, 255), cv2.FILLED)
                return x, y, z

            x1 = y1 = z1 = x2 = y2 = z2 = 0
            index = 0
            if len(my_list) > 1:
                for kn in range(len(my_list)):
                    if my_list[kn][0] == 'Right':
                        index = kn
                    print(index)
            else:
                if my_list[0][0] == 'Right':
                    index = 0

            x1, y1, z1 = finger_point(8, index)
            x2, y2, z2 = finger_point(5, index)
            x3, y3, z3 = finger_point(0, index)

            dist = math.sqrt((x1 - x2) ** 2 + (y1 - y2) ** 2)
            dist2 = math.sqrt((x2 - x3) ** 2 + (y2 - y3) ** 2)
            long = (z1 + z2) / 2 * 100
            k = dist / dist2
            scale = 160 * k

            cv2.line(t_image, (x1, y1), (x2, y2), (255, 0, 255), 3)
            cv2.line(t_image, (x2, y2), (x3, y3), (255, 0, 255), 3)
            cv2.putText(t_image, str(int(dist)), (30, 50),
                        cv2.FONT_HERSHEY_COMPLEX, 0.5, (255, 0, 0), 1, cv2.LINE_AA)
            cv2.putText(t_image, str(scale), (30, 80),
                        cv2.FONT_HERSHEY_COMPLEX, 0.5, (255, 0, 0), 1, cv2.LINE_AA)
            cv2.putText(t_image, str(int(dist2)), (30, 110),
                        cv2.FONT_HERSHEY_COMPLEX, 0.5, (255, 0, 0), 1, cv2.LINE_AA)

        return t_image


cam = cv2.VideoCapture(1)
track = analog_hand(cam, 0.6, 0.8)
while True:
    image = track.analog()
    cv2.imshow('hand', image)

    if cv2.waitKey(1) & 0xff == ord('q'):
        break

cam.release()
cv2.destroyAllWindows()
