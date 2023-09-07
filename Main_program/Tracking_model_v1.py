import cv2
import mediapipe as mp

mp_drawing = mp.solutions.drawing_utils
mp_hands = mp.solutions.hands


class Media:
    def __init__(self, camera, MDC=0.5, MTC=0.5):
        self.image = 0
        self.my_list = []
        self.camera = camera
        self.hands = mp_hands.Hands(
            min_detection_confidence=MDC,
            min_tracking_confidence=MTC)

    def tracking(self):
        self.my_list = []
        success, image = self.camera.read()
        image = cv2.flip(image, 1)
        image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

        image.flags.writeable = False
        results = self.hands.process(image)

        image.flags.writeable = True
        image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)

        if results.multi_hand_landmarks:
            for idx, hand_landmarks in enumerate(results.multi_hand_landmarks):
                num = idx
                mp_drawing.draw_landmarks(
                    image, hand_landmarks, mp_hands.HAND_CONNECTIONS)

        if results.multi_hand_landmarks:
            myHand = results.multi_hand_landmarks[0]
            for idx, lm in enumerate(myHand.landmark):
                h, w, c = image.shape
                cx = int(lm.x * w)
                cy = int(lm.y * h)
                cz = float(lm.z * c)
                self.my_list.append([idx, cx, cy, cz])
        return image
