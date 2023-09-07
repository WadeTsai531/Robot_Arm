import math
import cv2
import mediapipe as mp

mp_drawing = mp.solutions.drawing_utils
mp_hands = mp.solutions.hands
# For video input:
cap = cv2.VideoCapture(0)
'''fourcc = cv2.VideoWriter_fourcc(*'MP4V')
out = cv2.VideoWriter('../Vision/video/Robot_Arm_test_v1.mp4', fourcc, 20.0, (640,  480))'''

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
                x, y = my_list[point][1], my_list[point][2]
                cv2.circle(image, (x, y), 13, (255, 0, 255), cv2.FILLED)
                # tt = str(x1) + ', ' + str(y1) + ', ' + str(int(z1 * 10000))
                return x, y


            def line(point1, point2, color):
                x1, y1 = cir(point1)
                x2, y2 = cir(point2)
                cv2.circle(image, (x2, y2), 13, (255, 0, 255), cv2.FILLED)
                cv2.line(image, (x1, y1), (x2, y2), color, 3)

                point_x = x1 - x2
                point_y = y1 - y2

                d = math.sqrt(point_x ** 2 + point_y ** 2)

                cv2.putText(image, str(int(d)),
                            (x1 - point_x // 2, y1 - point_y // 2),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.5, color, 1, cv2.LINE_AA)
                return d

            def rec():
                L = []
                st = []
                for i in range(1, 11):
                    x, y = cir(i * 2)
                    L.append([x, y])
                cv2.putText(image, 'fig_1 = ' + str(L[0][0] - L[1][0]), (30, 50),
                            cv2.FONT_HERSHEY_SIMPLEX,
                            0.5, (255, 0, 255), 1, cv2.LINE_AA)
                st.append(L[0][0] - L[1][0])
                for k in range(2, 9, 2):
                    st.append(L[k][1] - L[k+1][1])
                    cv2.putText(image, 'fig ' + str(k//2+1)+' = '+str(st), (30, 60 + k*10),
                                cv2.FONT_HERSHEY_SIMPLEX,
                                0.5, (255, 0, 255), 1, cv2.LINE_AA)
                return st

            pt = rec()
            if pt[0] > 0:
                cv2.putText(image, 'Finger 1 up', (30, 170),
                            cv2.FONT_HERSHEY_SIMPLEX,
                            0.5, (255, 0, 255), 1, cv2.LINE_AA)
            if pt[1] > 0:
                cv2.putText(image, 'Finger 2 up', (30, 190),
                            cv2.FONT_HERSHEY_SIMPLEX,
                            0.5, (255, 0, 255), 1, cv2.LINE_AA)
            if pt[2] > 0:
                cv2.putText(image, 'Finger 3 up', (30, 210),
                            cv2.FONT_HERSHEY_SIMPLEX,
                            0.5, (255, 0, 255), 1, cv2.LINE_AA)
            if pt[3] > 0:
                cv2.putText(image, 'Finger 4 up', (30, 230),
                            cv2.FONT_HERSHEY_SIMPLEX,
                            0.5, (255, 0, 255), 1, cv2.LINE_AA)
            if pt[4] > 0:
                cv2.putText(image, 'Finger 5 up', (30, 250),
                            cv2.FONT_HERSHEY_SIMPLEX,
                            0.5, (255, 0, 255), 1, cv2.LINE_AA)

        cv2.imshow('MediaPipe Hands', image)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

cap.release()
cv2.destroyAllWindows()
