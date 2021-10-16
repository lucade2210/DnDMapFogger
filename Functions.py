import cv2
from math import *
import numpy as np
import random

def drawLine(image, x, y, coordinateList):
    cv2.line(image, (x, y), coordinateList[-1], (255, 255, 0), 1)

def drawText(image, x, y):
    cv2.putText(image, 'Start', (x, y), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 0), 1, cv2.LINE_AA)

def great_circle_distance(coords1, coords2):
    d = pi / 180
    answer =  acos(sin(coords1[1]*d) * sin(coords2[1]*d) +
              cos(coords1[1]*d) * cos(coords2[1]*d) *
              cos((coords1[0] - coords2[0]) * d)) / d
    return answer

def checkCoordinatesListInRange(x, y, coordinateList, range):
    for coords in coordinateList:
        if great_circle_distance((x, y), coords) < range:
            return True
    return False
            
def drawShape(imgShaped, coordinateList):
    pts =  [np.array([list(elem) for elem in coordinateList], np.int32)]
    B = random.randint(0, 255)
    G = random.randint(0, 255)
    R = random.randint(0, 255)
    cv2.fillPoly(imgShaped, pts, (B, G, R))
    

