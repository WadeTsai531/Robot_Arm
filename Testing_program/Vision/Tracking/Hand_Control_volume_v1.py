import time
import math
import cv2
import numpy as np
import mediapipe as mp
from ctypes import cast, POINTER
from comtypes import CLSCTX_ALL
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume

'''
    Use to control volume
'''

devices = AudioUtilities.GetSpeakers()
interface = devices.Activate(
    IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
volume = cast(interface, POINTER(IAudioEndpointVolume))
volRange = volume.GetVolumeRange()
volume.SetMasterVolumeLevel(0, None)
minVol = volRange[0]
maxVol = volRange[1]


mp_drawing = mp.solutions.drawing_utils
mp_hands = mp.solutions.hands
pTime = 0
# For video input:
cap = cv2.VideoCapture(1)
cap.set(3, 320)
cap.set(4, 320)
with mp_hands.Hands(
        min_detection_confidence=0.7,
        min_tracking_confidence=0.7) as hands:
    while True:
        success, image = cap.read()
        image = cv2.flip(image, 1)
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

        my_list = []
        if results.multi_hand_landmarks:
            myHand = results.multi_hand_landmarks[0]
            for idx, lm in enumerate(myHand.landmark):
                h, w, c = image.shape
                cx, cy = int(lm.x * w), int(lm.y * h)
                # print(idx, cx, cy)
                my_list.append([idx, cx, cy])
                # print(my_list[idx])

        if len(my_list) != 0:
            x1, y1 = my_list[8][1], my_list[8][2]
            x2, y2 = my_list[4][1], my_list[4][2]

            point_1 = my_list[8][1] - my_list[4][1]
            point_2 = my_list[8][2] - my_list[4][2]
            # print(my_list[8][1] - my_list[5][1], my_list[8][2]-my_list[5][2])
            d = math.hypot(x2-x1, y2-y1)

            cv2.circle(image, (x1, y1), 13, (255, 0, 255), cv2.FILLED)
            cv2.circle(image, (x2, y2), 13, (255, 0, 255), cv2.FILLED)
            cv2.line(image, (x1, y1), (x2, y2), (255, 0, 255), 3)
            cv2.putText(image, str(int(d)), (x1+40, y1), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 0, 255), 1, cv2.LINE_AA)

            vol = np.interp(d, [20, 200], [minVol, maxVol])
            print(int(d), vol)
            volume.SetMasterVolumeLevel(vol, None)

        cv2.putText(image, f'FPS: {int(fps)}', (30, 50), cv2.FONT_HERSHEY_COMPLEX, 1, (255, 0, 0), 0)
        cv2.imshow('MediaPipe Hands', image)
        
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

cap.release()
cv2.destroyAllWindows()
