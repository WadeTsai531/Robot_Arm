import os
import cv2
import time
import keyboard

save_path = 'pic/test_3'  # 照片存取位置
cam = cv2.VideoCapture(0)
num = 0

while True:
    ret, img = cam.read()

    if keyboard.is_pressed('c'):    # 按下 c 截圖
        time.sleep(0.5)
        img_name = os.path.join(save_path, 'temp'+str(num)+'.jpg')
        cv2.imwrite(img_name, img)
        print('Save !!!')
        num += 1

    cv2.imshow('face', img)
    if cv2.waitKey(1) & 0xff == ord('q'):   # 按下 q 停止程式
        break

cam.release()
cv2.destroyAllWindows()
