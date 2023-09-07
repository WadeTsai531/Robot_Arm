from Track_package import Tracking_model_v2 as TM2
import cv2
import serial


class Hand_Track(TM2.Media):
    def __init__(self, camera):
        super().__init__(camera)
        self.flag = {'Right': False,
                     'Left': False,
                     'Middle': True}

    def nor(self):
        return super().tracking()

    def slide(self):
        t_image = super().tracking()
        my_list = self.my_dir

        def cir(point):
            x, y = my_list[0][1][point][1], my_list[0][1][point][2]
            cv2.circle(t_image, (x, y), 10, (255, 0, 0), cv2.FILLED)
            return x, y

        cv2.line(t_image, (150, 0), (150, 480), (255, 0, 0), 2)
        cv2.line(t_image, (490, 0), (490, 480), (255, 0, 0), 2)

        if len(my_list) != 0 and my_list[0][0] == 'Right':
            x, y = cir(9)
            if 150 < x < 490:
                if not self.flag['Middle']:
                    self.flag['Middle'] = True
                    print('Middle')
            else:
                if self.flag['Middle']:
                    self.flag['Middle'] = False

            if x > 490:
                if not self.flag['Right']:
                    self.flag['Right'] = True
                    print('Right')
                print((x - 490), (x - 490)//10)
            else:
                if self.flag['Right']:
                    self.flag['Right'] = False

            if x < 150:
                if not self.flag['Left']:
                    self.flag['Left'] = True
                    print('Left')
            else:
                if self.flag['Left']:
                    self.flag['Left'] = False

        return t_image


cam = cv2.VideoCapture(1)
track = Hand_Track(cam)

while True:
    image = track.slide()
    cv2.imshow('Hand', image)

    if cv2.waitKey(1) & 0xff == ord('q'):
        break
cam.release()
cv2.destroyAllWindows()
