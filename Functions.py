import cv2
from math import *
import numpy as np
import cupy as cp

def drawLine(image, x, y, coordinateList):
    return cp.array(cv2.line(cp.asnumpy(image), (x, y), coordinateList[-1], (255,0,0), 2))

def drawText(image, x, y):
    return cp.array(cv2.putText(cp.asnumpy(image), 'Start', (x, y), cv2.FONT_HERSHEY_SIMPLEX, 1, (255,0,0), 2, cv2.LINE_AA))

def drawDot(image, x, y, radius):
    return cp.array(cv2.circle(cp.asnumpy(image), (x, y), radius, (1,1,1), thickness=cv2.FILLED))
    
def drawShape(image, coordinateList):
    pts =  [np.array([list(elem) for elem in coordinateList], np.int32)]
    return cp.array(cv2.fillPoly(cp.asnumpy(image), pts, (1,1,1)))

def checkCoordinatesWithStart(x, y, coordinateList, clickRange):
    coords = coordinateList[0]
    if coords[0] - clickRange <= x <= coords[0] + clickRange and coords[1] - clickRange <= y <= coords[1] + clickRange:
        return True
    return False

def overlayMask(mask, imgOnZero, imgOnOne):
    return cp.where(mask, imgOnOne, imgOnZero)

def overlayMaskWeighted(mask, imgOnZero, imgOnOne):
    return np.around(mask * imgOnOne + (1-mask) * imgOnZero,0)

def overlayMaskRaw(mask, imgOnZero, imgOnOne):
    return cp.asnumpy(cp.where(cp.array(mask), cp.array(imgOnOne), cp.array(imgOnZero)))

