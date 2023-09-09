import os
import cv2
import time
import keyboard

save_path = 'pic/test_3'
cam = cv2.VideoCapture(1)
num = 0

while True:
    ret, img = cam.read()

    if keyboard.is_pressed('c'):
        time.sleep(0.5)
        img_name = os.path.join(save_path, 'temp'+str(num)+'.jpg')
        cv2.imwrite(img_name, img)
        print('Save !!!')
        num += 1

    cv2.imshow('face', img)
    if cv2.waitKey(1) & 0xff == ord('q'):
        break

cam.release()
cv2.destroyAllWindows()
