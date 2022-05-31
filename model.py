import cv2 as cv
import numpy as np
import picture as pic
import vector as vec
import getcontour as con


def write_model_img_feature():
    cap = cv.VideoCapture(0)
    model_num = './' + 'model_number' + '/' + 'count.txt'
    n = open(model_num, 'r')
    i = int(n.read())
    n.close()
    while True:
        ret, frame = cap.read()
        frame = cv.flip(frame, 1)
        cv.rectangle(frame, (400, 60), (640, 300), (200, 100, 0))
        cv.imshow('write_model_img', frame)
        frame = frame[60:300, 400:640]
        k = cv.waitKey(1)

        if k == ord('t'):
            break
        elif k == ord('s'):
            imname = './' + 'model_pic' + '/'+str(i)+'.jpg'
            bole = cv.imwrite(imname, frame)
            if bole==True:
                print('已存入照片')
                handle_model_vec(i)
                i += 1

    f = open(model_num, 'w')
    f.write(str(i))
    f.close()

    cap.release()
    cv.destroyAllWindows()


def handle_model_vec(i):
    imname = './' + 'model_pic' + '/' + str(i) + '.jpg'
    img = cv.imread(imname)
    im1 = pic.pic_handle(img)
    contour_max, defects = con.find_contours(im1, img)
    collect_vec = vec.create_vector(im1, contour_max, defects, True)
    fname = './' + 'feature' + '/' + str(i) + '.txt'
    f = open(fname, 'w')
    f.write(str(collect_vec[0])+','+str(collect_vec[1])+','+str(collect_vec[2])+','+str(collect_vec[3])+','+str(collect_vec[4])+','+str(collect_vec[5]))
    f.close()


if __name__ == "__main__":
    write_model_img_feature()

