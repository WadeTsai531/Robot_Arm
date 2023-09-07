import Tracking_model_v1 as tm1
import Tracking_model_v2 as tm2
import cv2
import math


class recon(tm2.Media):
    def __init__(self, camera, mdc, mtc):
        super().__init__(camera, mdc, mtc)

    def trr(self):
        return super().tracking()

    def recog(self):
        my_list = self.my_list
        image_re = super().tracking()
        if len(my_list) != 0:
            def cir(point):
                x, y = my_list[point][1], my_list[point][2]
                cv2.circle(image_re, (x, y), 13, (255, 0, 255), cv2.FILLED)
                # tt = str(x1) + ', ' + str(y1) + ', ' + str(int(z1 * 10000))
                return x, y

            def line(point1, point2, color):
                x1, y1 = cir(point1)
                x2, y2 = cir(point2)
                cv2.circle(image_re, (x2, y2), 13, (255, 0, 255), cv2.FILLED)
                cv2.line(image_re, (x1, y1), (x2, y2), color, 3)

                point_x = x1 - x2
                point_y = y1 - y2

                d = math.sqrt(point_x ** 2 + point_y ** 2)

                cv2.putText(image_re, str(int(d)),
                            (x1 - point_x // 2, y1 - point_y // 2),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.5, color, 1, cv2.LINE_AA)
                return d

            def rec():
                L = []
                st = []
                for i in range(1, 11):
                    x, y = cir(i * 2)
                    L.append([x, y])
                cv2.putText(image_re, 'fig_1 = ' + str(L[0][0] - L[1][0]), (30, 50),
                            cv2.FONT_HERSHEY_SIMPLEX,
                            0.5, (255, 0, 255), 1, cv2.LINE_AA)
                st.append(L[0][0] - L[1][0])
                for k in range(2, 9, 2):
                    st.append(L[k][1] - L[k + 1][1])
                    cv2.putText(image_re, 'fig ' + str(k // 2 + 1) + ' = ' + str(st), (30, 60 + k * 10),
                                cv2.FONT_HERSHEY_SIMPLEX,
                                0.5, (255, 0, 255), 1, cv2.LINE_AA)
                return st

            pt = rec()
            if pt[0] > 0:
                cv2.putText(image_re, 'Finger 1 up', (30, 170),
                            cv2.FONT_HERSHEY_SIMPLEX,
                            0.5, (255, 0, 255), 1, cv2.LINE_AA)
            if pt[1] > 0:
                cv2.putText(image_re, 'Finger 2 up', (30, 190),
                            cv2.FONT_HERSHEY_SIMPLEX,
                            0.5, (255, 0, 255), 1, cv2.LINE_AA)
            if pt[2] > 0:
                cv2.putText(image_re, 'Finger 3 up', (30, 210),
                            cv2.FONT_HERSHEY_SIMPLEX,
                            0.5, (255, 0, 255), 1, cv2.LINE_AA)
            if pt[3] > 0:
                cv2.putText(image_re, 'Finger 4 up', (30, 230),
                            cv2.FONT_HERSHEY_SIMPLEX,
                            0.5, (255, 0, 255), 1, cv2.LINE_AA)
            if pt[4] > 0:
                cv2.putText(image_re, 'Finger 5 up', (30, 250),
                            cv2.FONT_HERSHEY_SIMPLEX,
                            0.5, (255, 0, 255), 1, cv2.LINE_AA)
        return image_re

    def sd(self):
        my_list = self.my_dir
        image_re = super().tracking()
        if len(my_list) != 0:
            def cir(point, rl):
                x, y = my_list[rl][1][point][1], my_list[rl][1][point][2]
                cv2.circle(image_re, (x, y), 13, (255, 0, 255), cv2.FILLED)
                return x, y

            if len(my_list) > 1:
                index_R = index_L = 0
                for kn in range(len(my_list)):
                    if my_list[kn][0] == 'Right':
                        index_R = kn
                    elif my_list[kn][0] == 'Left':
                        index_L = kn
                cir(5, index_L)
                cir(3, index_R)
            else:
                if my_list[0][0] == 'Right':
                    cir(3, 0)

        return image_re


cam = cv2.VideoCapture(0)
track = recon(cam, 0.8, 0.5)
while True:
    image = track.sd()  # track.recog()
    cv2.imshow('sda', image)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
