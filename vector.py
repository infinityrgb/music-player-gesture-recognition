import cv2 as cv
import numpy as np
import math


def _get_eucledian_distance__tuple(start, end):
    return np.sqrt(np.sum(np.square(np.array(start) - np.array(end))))


def calculate_finger2(array, contour, defects, verbose=True):
    ndefects = 0
    s, e, f, _ = defects[defects.shape[0]-1, 0]
    last_end = tuple(contour[e][0])
    for i in range(defects.shape[0]):
        s, e, f, _ = defects[i, 0]
        start = tuple(contour[s][0])
        end = tuple(contour[e][0])
        far = tuple(contour[f][0])
        a = _get_eucledian_distance__tuple(start, end)
        b = _get_eucledian_distance__tuple(start, far)
        c = _get_eucledian_distance__tuple(end, far)
        last_dis = _get_eucledian_distance__tuple(start, last_end)
        angle = math.acos((b ** 2 + c ** 2 - a ** 2) / (2 * b * c))
        if (angle <= math.pi / 2)and(last_dis < 20):
            ndefects = ndefects + 1
            '''
            if verbose:
                cv.circle(array, far, 3, (0, 255, 0), -1)
                cv.imshow("image2", array)
        if verbose:
            cv.line(array, start, end, (0, 255, 0), 1)
            cv.imshow("image2", array)
            '''
        cv.imshow('calculate_finger2', array)
        last_end = end
    return ndefects+1


def length_area(contour):
    l = cv.arcLength(contour, closed=True)
    area = abs(cv.contourArea(contour))
    r = l * l / (4 * 3.14 * area)
    return r


def get_hu(contour):
    moments = cv.moments(contour)
    hu_moments = cv.HuMoments(moments)
    return hu_moments


def create_vector(img, contour, defects, verbose=True):
    ndefects = calculate_finger2(img, contour, defects, verbose=True)
    len_area = length_area(contour)
    hu_moments = get_hu(contour)
    m1 = hu_moments[0][0]
    m2 = hu_moments[1][0]
    m3 = hu_moments[2][0]
    m4 = hu_moments[3][0]
    x = [m1, m2, m3, m4, ndefects, len_area]
    return x
