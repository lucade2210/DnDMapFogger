import cv2
from math import *
import numpy as np

def drawLine(image, x, y, coordinateList):
    cv2.line(image, (x, y), coordinateList[-1], (255,0,0), 2)

def drawText(image, x, y):
    cv2.putText(image, 'Start', (x, y), cv2.FONT_HERSHEY_SIMPLEX, 1, (255,0,0), 2, cv2.LINE_AA)

def drawDot(image, x, y, radius):
    cv2.circle(image, (x, y), radius, (255,0,0), 2)
    
def drawShape(img, coordinateList):
    pts =  [np.array([list(elem) for elem in coordinateList], np.int32)]
    cv2.fillPoly(img, pts, (1,1,1))

def checkCoordinatesWithStart(x, y, coordinateList, clickRange):
    coords = coordinateList[0]
    if coords[0] - clickRange <= x <= coords[0] + clickRange and coords[1] - clickRange <= y <= coords[1] + clickRange:
        return True
    return False
            
def overlayMask(mask, imgOnZero, imgOnOne):
    return np.where(mask, imgOnOne, imgOnZero)
