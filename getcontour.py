# 轮廓提取
import cv2 as cv
import numpy as np
import matplotlib.pyplot as plt
import math


def find_contours(pic, begin_pic):
    binaryimg = cv.Canny(pic, 50, 200)
    contours, hierarchy = cv.findContours(binaryimg, cv.RETR_TREE, cv.CHAIN_APPROX_NONE)
    contour = sorted(contours, key=cv.contourArea, reverse=True)
    contour_max = contour[0]
    hull = cv.convexHull(contour_max)
    hulls = cv.convexHull(contour_max, clockwise=True, returnPoints=False)
    defects = cv.convexityDefects(contour_max, hulls)
    cv.drawContours(begin_pic, contour_max, -1, (0, 0, 255), 2)
    cv.drawContours(begin_pic, [hull], -1, (255, 0, 0), 2)
    # cv.imshow('drawContours', begin_pic)
    return contour_max, defects
