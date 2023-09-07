import time
import math
import cv2
import numpy as np
import mediapipe as mp

mp_drawing = mp.solutions.drawing_utils
mp_hands = mp.solutions.hands
pTime = 0
# For video input:
cap = cv2.VideoCapture('video_test1.mp4')
with mp_hands.Hands(
        min_detection_confidence=0.5,
        min_tracking_confidence=0.5) as hands:
    while cap.isOpened():
        success, image = cap.read()
        cTime = time.time()
        fps = 1 / (cTime - pTime)
        pTime = cTime
        image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

        image.flags.writeable = False
        results = hands.process(image)

        image.flags.writeable = True
        image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)

        if results.multi_hand_landmarks:
            for hand_landmarks in results.multi_hand_landmarks:
                mp_drawing.draw_landmarks(
                    image, hand_landmarks, mp_hands.HAND_CONNECTIONS)

        if results.multi_hand_landmarks:
            my_list = []
            myHand = results.multi_hand_landmarks[0]
            for idx, lm in enumerate(myHand.landmark):
                h, w, c = image.shape
                cx, cy = int(lm.x * w), int(lm.y * h)
                # print(idx, cx, cy)
                my_list.append([idx, cx, cy])
                # print(my_list[idx])

        point_1 = my_list[8][1] - my_list[5][1]
        point_2 = my_list[8][2]-my_list[5][2]
        # print(my_list[8][1] - my_list[5][1], my_list[8][2]-my_list[5][2])

        d = math.sqrt(point_1 ** 2 + point_2 ** 2)
        print(d)

        cv2.putText(image, f'FPS: {int(fps)}', (30, 50), cv2.FONT_HERSHEY_COMPLEX, 1, (255, 0, 0), 0)
        cv2.imshow('MediaPipe Hands', image)
        
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

cap.release()
cv2.destroyAllWindows()
