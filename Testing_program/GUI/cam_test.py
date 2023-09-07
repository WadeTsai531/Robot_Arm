import cv2

cam = cv2.VideoCapture(0)

while True:
    ret, image = cam.read()
    cv2.imshow('sada', image)
    if cv2.waitKey(1) == ord('q'):
        break

cv2.destroyAllWindows()
