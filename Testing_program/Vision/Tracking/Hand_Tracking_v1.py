import time

import cv2
import numpy as np
import mediapipe as mp

fourcc = cv2.VideoWriter_fourcc(*'XVID')
out = cv2.VideoWriter('output.avi', fourcc, 30.0, (540,  960))


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
        fps = 1/(cTime-pTime)
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

        cv2.putText(image, f'FPS: {int(fps)}', (30, 50), cv2.FONT_HERSHEY_COMPLEX, 1, (255, 0, 0), 0)
        cv2.imshow('MediaPipe Hands', image)
        out.write(image)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
out.release()
cap.release()
cv2.destroyAllWindows()

