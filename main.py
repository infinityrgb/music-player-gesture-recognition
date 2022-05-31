import math
import time
import cv2 as cv
import picture as pic
import getcontour as con
import vector as vec
import numpy as np
geshu = 0


def eucledian_distance(x, y):
    pip = np.sqrt(np.sum(np.square(np.array(x) - np.array(y))))
    return pip


def read_model_feature(i):
    fname = './' + 'feature' + '/' + str(i) + '.txt'
    f = open(fname, 'r')
    vec_str = f.read()
    f.close()
    vec_array = vec_str.split(',')
    vec_array = list(map(float, vec_array))
    return vec_array


def recognise(img, verbose=True):
    global geshu
    geshu = geshu + 1
    model_num = './' + 'model_number' + '/' + 'count.txt'
    n = open(model_num, 'r')
    i = int(n.read())
    n.close()
    # time.sleep(0.001)
    img1 = pic.pic_handle(img)
    contour_max, defects = con.find_contours(img1, img)
    if cv.contourArea(contour_max) < 2000:
        return 9
    if defects is not None:
        ve = vec.create_vector(img1, contour_max, defects, verbose=True)
        dist = []
        for k in range(0, i):
            model_vec = read_model_feature(k)
            eucledian = eucledian_distance(ve, model_vec)
            dist.append(eucledian)
        min = 0
        for p in range(0, i):
            if dist[p] < dist[min]:
                min = p

        fname = './' + 'feature' + '/' + str(min) + '.txt'
        feature = open(fname,  'r')
        sttr = feature.read()
        feature.close()
        hand_feature = sttr.split(',')
        if min == 0:
            hand_num = 0
        else:
            hand_num = int(hand_feature[4])
        print('The hand is :' + str(hand_num))
        return hand_num


if __name__ == "__main__":
    shumu = 0
    camera = cv.VideoCapture(0,cv.CAP_DSHOW)
    while camera.isOpened():
        ret, frame = camera.read()
        frame = cv.flip(frame, 1)
        cv.rectangle(frame, (400, 60), (640, 300), (200, 100, 0))
        cv.imshow('camera', frame)
        img = frame[60:300, 400:640]

        hand_num = recognise(img, True)
        # if hand_num == 5:
            # shumu += 1
        if cv.waitKey(1) & 0xff == ord("x"):
            break
        # print('总个数:'+str(geshu)+'5的数目'+str(shumu))
    camera.release()
    cv.destroyAllWindows()
