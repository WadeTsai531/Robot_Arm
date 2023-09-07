import Tracking_model_v2 as TM2
import cv2
import math


class Hand_Track(TM2.Media):
    def __init__(self, camera, mdc, mtc):
        super().__init__(camera, mdc, mtc)

    def normal(self):
        return super().tracking()

    def analog(self):
        my_list = self.my_dir
        t_image = super().tracking()

        if len(my_list) != 0 and my_list[0][0] == 'Right':
            def finger_point(point, R_L=0):
                x, y = my_list[R_L][1][point][1], \
                          my_list[R_L][1][point][2]
                cv2.circle(t_image, (x, y), 12, (255, 0, 255), cv2.FILLED)
                return x, y

            def distance(point_1, point_2):
                x1, y1 = finger_point(point_1)
                x2, y2 = finger_point(point_2)
                dist = math.sqrt((x1 - x2) ** 2 + (y1 - y2) ** 2)
                return dist

            def dist_comp(point_1, point_2):
                dist_1 = distance(point_1, point_2)
                dist_2 = distance(point_1 + 1, point_2)
                if dist_2 > dist_1:
                    return True
                else:
                    return False

            finger = [[5, 8], [9, 12], [13, 16], [17, 20]]
            rcog = []
            T_dist_1 = distance(4, 13)
            T_dist_2 = distance(4, 5)
            if T_dist_2+10 > T_dist_1 or T_dist_2 < 20:
                rcog.append(True)
            else:
                rcog.append(False)

            for num in finger:
                rcog.append(dist_comp(num[0], num[1]))

            recognition = {'Zero': [True, True, True, True, True],
                           'One': [True, False, True, True, True],
                           'Two': [True, False, False, True, True],
                           'Three': [True, False, False, False, True],
                           'Four': [True, False, False, False, False],
                           'Five': [False, False, False, False, False],
                           'Six': [False, True, True, True, False],
                           'Seven': [False, False, True, True, True],
                           'Eight': [False, False, False, True, True],
                           'Nine': [False, False, False, False, True]}

            for check in recognition:
                if recognition[check] == rcog:
                    print(check)

        return t_image


cam = cv2.VideoCapture(0)
track = Hand_Track(cam, 0.6, 0.8)
while True:
    image = track.analog()
    cv2.imshow('hand', image)

    if cv2.waitKey(1) & 0xff == ord('q'):
        break

cam.release()
cv2.destroyAllWindows()
