import cv2
from math import *
import numpy as np
import random

def drawLine(image, x, y, coordinateList):
    cv2.line(image, (x, y), coordinateList[-1], (255,0,0), 2)

def drawText(image, x, y):
    cv2.putText(image, 'Start', (x, y), cv2.FONT_HERSHEY_SIMPLEX, 1, (255,0,0), 2, cv2.LINE_AA)

def checkCoordinatesListInRange(x, y, coordinateList, clickRange):
    for coords in coordinateList:
        if coords[0] - clickRange <= x <= coords[0] + clickRange and coords[1] - clickRange <= y <= coords[1] + clickRange:
            return True
    return False
            
def drawShape(img, coordinateList):
    pts =  [np.array([list(elem) for elem in coordinateList], np.int32)]
    cv2.fillPoly(img, pts, (0,0,0))

def overlayMask(mask, img, imgOG, color):
    img = np.where(mask == 0, imgOG, color)
    return img

def overlayMaskTransparent(mask, img, imgOG):
    img = np.where(mask != 0, imgOG, img)
    return img
    

