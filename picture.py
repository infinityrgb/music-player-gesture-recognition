import cv2 as cv
import numpy as np


def pic_handle(pic):
    frame = cv.bilateralFilter(pic, 5, 50, 100)
    kernel = np.array([[0, -1, 0], [-1, 5, -1], [0, -1, 0]], np.float32)
    dst = cv.filter2D(frame, -1, kernel=kernel)
    # cv.imshow('first', dst)
    img = skin_mask(dst)
    # cv.imshow('skin_mask', img)
    img = shape_handle(img)
    # cv.imshow('shape_handle', img)
    return img


def skin_mask(roi):
    YCrCb = cv.cvtColor(roi, cv.COLOR_BGR2YCR_CB)
    (y, cr, cb) = cv.split(YCrCb)
    cr1 = cv.GaussianBlur(cr, (5, 5), 0)
    _, skin = cv.threshold(cr1, 0, 255, cv.THRESH_OTSU)
    return skin


def shape_handle(pic):
    kernel = np.ones((5, 5), np.uint8)
    closing = cv.morphologyEx(pic, cv.MORPH_CLOSE, kernel)
    openning = cv.morphologyEx(closing, cv.MORPH_OPEN, kernel)
    return openning
