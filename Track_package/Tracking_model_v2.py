import cv2
import mediapipe as mp

mp_drawing = mp.solutions.drawing_utils
mp_hands = mp.solutions.hands


class Media:
    def __init__(self, camera, MDC=0.5, MTC=0.5):
        self.image = 0
        self.my_dir = []
        self.camera = camera
        self.hands = mp_hands.Hands(
            static_image_mode=False,
            max_num_hands=1,
            min_detection_confidence=MDC,
            min_tracking_confidence=MTC)

    def tracking(self):
        self.my_dir = []
        success, image = self.camera.read()
        image = cv2.flip(image, 1)
        image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

        image.flags.writeable = False
        results = self.hands.process(image)

        image.flags.writeable = True
        image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)

        if results.multi_hand_landmarks:
            for hand_idx, hand_landmarks in enumerate(results.multi_hand_landmarks):
                my_list = []
                mp_drawing.draw_landmarks(
                    image, hand_landmarks, mp_hands.HAND_CONNECTIONS)
                mm = results.multi_handedness[hand_idx].classification
                myHand = results.multi_hand_landmarks[hand_idx]
                for fig_idx, lm in enumerate(myHand.landmark):
                    h, w, c = image.shape
                    cx = int(lm.x * w)
                    cy = int(lm.y * h)
                    cz = float(lm.z * c)
                    my_list.append([fig_idx, cx, cy, cz])
                self.my_dir.append([mm[0].label, my_list])
        return image
