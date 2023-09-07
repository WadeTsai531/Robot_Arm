"""
    Testing z distance

"""

import time
import math
import cv2
import numpy as np
import mediapipe as mp

mp_drawing = mp.solutions.drawing_utils
mp_hands = mp.solutions.hands
pTime = 0

z_max = 0
z_min = 2000
# For video input:
cap = cv2.VideoCapture(0)
fourcc = cv2.VideoWriter_fourcc(*'MP4V')
out = cv2.VideoWriter('../Vision/video/Robot_Arm_test_v1.mp4',
                      fourcc, 20.0, (640,  480))

with mp_hands.Hands(
        min_detection_confidence=0.7,
        min_tracking_confidence=0.7) as hands:
    while True:
        success, image = cap.read()
        image = cv2.flip(image, 1)
        image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

        image.flags.writeable = False
        results = hands.process(image)

        image.flags.writeable = True
        image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)

        if results.multi_hand_landmarks:
            for hand_landmarks in results.multi_hand_landmarks:
                mp_drawing.draw_landmarks(
                    image, hand_landmarks, mp_hands.HAND_CONNECTIONS)

        my_list = []
        if results.multi_hand_landmarks:
            myHand = results.multi_hand_landmarks[0]
            for idx, lm in enumerate(myHand.landmark):
                h, w, c = image.shape
                cx, cy = int(lm.x * w), int(lm.y * h)
                cz = float(lm.z * c)
                # print(idx, cx, cy)
                my_list.append([idx, cx, cy, cz])
                # print(my_list[idx])

        if len(my_list) != 0:
            def cir(point):
                x, y, z = my_list[point][1], my_list[point][2], my_list[point][3]
                cv2.circle(image, (x, y), 13, (255, 0, 255), cv2.FILLED)
                # tt = str(x1) + ', ' + str(y1) + ', ' + str(int(z1 * 10000))
                return x, y, z


            def line(point1, point2, color):
                x1, y1, z1 = cir(point1)
                x2, y2, z2 = cir(point2)
                cv2.circle(image, (x2, y2), 13, (255, 0, 255), cv2.FILLED)
                cv2.line(image, (x1, y1), (x2, y2), color, 3)

                point_x = x1 - x2
                point_y = y1 - y2

                d = math.sqrt(point_x ** 2 + point_y ** 2)

                cv2.putText(image, str(int(d)),
                            (x1 - point_x // 2, y1 - point_y // 2),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.5, color, 1, cv2.LINE_AA)
                return d


            def TR():
                x1, y1, z1 = cir(0)
                x2, y2, z2 = cir(5)
                x3, y3, z3 = cir(17)
                cv2.line(image, (x1, y1), (x2, y2), (255, 146, 133), 3)
                cv2.line(image, (x2, y2), (x3, y3), (255, 146, 133), 3)
                cv2.line(image, (x1, y1), (x3, y3), (255, 146, 133), 3)

                point_ax = x1 - x2
                point_ay = y1 - y2
                d_a = math.sqrt(point_ax ** 2 + point_ay ** 2)

                point_bx = x2 - x3
                point_by = y2 - y3
                d_b = math.sqrt(point_bx ** 2 + point_by ** 2)

                point_cx = x1 - x3
                point_cy = y1 - y3
                d_c = math.sqrt(point_cx ** 2 + point_cy ** 2)

                s = (d_a + d_b + d_c) / 2
                area = math.sqrt(s*(s-d_a)*(s-d_b)*(s-d_c))

                cv2.putText(image, 'area = ' + str(area), (20, 20),
                            cv2.FONT_HERSHEY_SIMPLEX,
                            0.5, (0, 76, 251), 1, cv2.LINE_AA)

            def z_avarig():
                z_lis = []
                z_av = 0
                ps = 50
                z_lis.append(my_list[0][3])
                for lis_n in range(5, 18, 4):
                    z_av += my_list[lis_n][3]
                    z_lis.append(my_list[lis_n][3])
                    '''cv2.putText(image, str(lis_n) + ' = ' + str(my_list[lis_n][3] * 1000),
                                (20, ps),
                                cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 76, 251), 1, cv2.LINE_AA)'''
                z_av = abs(z_av * 10000 // 5)
                '''cv2.putText(image, 'z = ' + str(z_av),
                            (20, 20),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 76, 251), 1, cv2.LINE_AA)'''
                return z_lis


            # TR()
            z_vv = z_avarig()

            d1 = line(0, 4, (255, 146, 133))
            d2 = line(0, 8, (0, 15, 255))
            d3 = line(0, 12, (0, 224, 255))
            d4 = line(0, 16, (0, 255, 70))
            d5 = line(0, 20, (255, 0, 182))

            k = 100
            d1 = (int(d1) - k) * 1.2
            if d1 > 130:
                d1 = 130
            elif d1 < 0:
                d1 = 0

            cv2.putText(image, 'd1 = ' + str(d1), (20, 40),
                        cv2.FONT_HERSHEY_SIMPLEX,
                        0.5, (0, 76, 251), 1, cv2.LINE_AA)

            '''
            x1, y1 = my_list[8][1], my_list[8][2]
            x2, y2 = my_list[4][1], my_list[4][2]

            point_1 = my_list[8][1] - my_list[4][1]
            point_2 = my_list[8][2] - my_list[4][2]
            # print(my_list[8][1] - my_list[5][1], my_list[8][2]-my_list[5][2])
            d = math.sqrt(point_1 ** 2 + point_2 ** 2)

            cv2.circle(image, (x1, y1), 13, (255, 0, 255), cv2.FILLED)
            cv2.circle(image, (x2, y2), 13, (255, 0, 255), cv2.FILLED)
            cv2.line(image, (x1, y1), (x2, y2), (255, 0, 255), 3)
            cv2.putText(image, str(int(d)), (x1+40, y1), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 0, 255), 1, cv2.LINE_AA)'''

        # cv2.putText(image, f'FPS: {int(fps)}', (30, 50), cv2.FONT_HERSHEY_COMPLEX, 1, (255, 0, 0), 0)
        cv2.imshow('MediaPipe Hands', image)
        # out.write(image)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

cap.release()
cv2.destroyAllWindows()
