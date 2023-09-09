import os
import cv2
import numpy as np
import face_recognition

path = '../pic/test_4'
images = []
classNames = []
my_list = os.listdir(path)
print(my_list)

for cl in my_list:
    curImg = cv2.imread(f'{path}/{cl}')
    images.append(curImg)
    classNames.append(os.path.splitext(cl)[0])


def Find_encoding(img_s):
    encode_list = []
    for img in img_s:
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        encode = face_recognition.face_encodings(img)[0]
        encode_list.append(encode)
    return encode_list


encode_list_know = Find_encoding(images)
print('Encoding Complete')

cam = cv2.VideoCapture(1)

while True:
    success, img = cam.read()
    img_resize = cv2.resize(img, (0, 0), None, 0.25, 0.25)
    img_RGB = cv2.cvtColor(img_resize, cv2.COLOR_BGR2RGB)

    face_cur_frame = face_recognition.face_locations(img_resize)
    encoding_cur_frame = face_recognition.face_encodings(img_RGB, face_cur_frame)

    for encode_face, face_Loc in zip(encoding_cur_frame, face_cur_frame):
        matches = face_recognition.compare_faces(encode_list_know, encode_face, tolerance=0.4)
        face_dis = face_recognition.face_distance(encode_list_know, encode_face)
        print(face_dis)
        match_index = np.argmin(face_dis)

        if matches[match_index]:
            name = classNames[match_index].upper()
            print(name)
            y1, x2, y2, x1 = face_Loc
            y1, x2, y2, x1 = y1*4, x2*4, y2*4, x1*4
            cv2.rectangle(img, (x1, y1), (x2, y2), (0, 255, 0), 2)
            cv2.rectangle(img, (x1, y2-35), (x2, y2), (0, 255, 0), cv2.FILLED)
            cv2.putText(img, name, (x1+6, y2-6), cv2.FONT_HERSHEY_COMPLEX, 1,
                        (255, 255, 255), 2)

    cv2.imshow('cam', img)
    if cv2.waitKey(1) & 0xff == ord('q'):
        break

cam.release()
cv2.destroyAllWindows()

