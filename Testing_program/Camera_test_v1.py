import cv2

cam = cv2.VideoCapture(0)

while True:
    ret, img = cam.read()
    cv2.imshow('cam', img)

    if cv2.waitKey(1) == ord('q'):
        break

cv2.destroyAllWindows()
