import cv2
import numpy as np
import cupy as cp
import os
import random
import Functions as f

class ImageSetArrays:

    def __init__(self, dim, imagePath):
        self.dim = dim
        self.dimX = dim[0]
        self.dimY = dim[1]
        self.clickRange = round(self.dimX / 150)

        self.imgOriginal = cv2.imread(imagePath) #OG unedited image
        self.imgBase = cv2.resize(self.imgOriginal, dim, interpolation = cv2.INTER_AREA) #resized image
        self.imgBaseDark = cv2.add(self.imgBase.copy(), np.array([-40.0])) #darkend image
        self.imgBase = cp.array(self.imgBase)
        self.imgBaseDark = cp.array(self.imgBaseDark)

        self.fogMask = cp.zeros((self.dimY, self.dimX, 3), cp.uint8) #masking shape arrays
        randomFile = "Fogs\\" + random.choice(os.listdir("Fogs\\"))
        self.imgFog = cp.array(cv2.resize(cv2.imread(randomFile), dim, interpolation = cv2.INTER_AREA)) #fog image


        self.imgViewer = self.imgFog.copy() #combined image for viewer
        self.imgDrawer = self.imgBaseDark.copy() #combined image for drawer
        self.imgDrawn = self.imgDrawer.copy() #temp image for drawer with drawn lines

        self.coordinateList = []

    def updateDrawerImage(self):
        cv2.imshow('drawer', cp.asnumpy(self.imgDrawn))

    def updateViewerImage(self):
        cv2.imshow('viewer', cp.asnumpy(self.imgViewer))

    def overlayFogMaskWithViewerVid(self, imgVid):
        self.imgViewer = f.overlayMask(self.fogMask, imgVid, self.imgBase)

    def resetDrawnImage(self):
        self.imgDrawn = self.imgDrawer.copy()
    
    def reload(self):
        self.coordinateList.clear()
        self.resetDrawnImage()
        self.updateDrawerImage()
        self.updateViewerImage()
    
    def rotate(self):
        self.imgOriginal = cp.array(cv2.rotate(self.imgOriginal, cv2.ROTATE_180))
        self.imgBase = cp.array(cv2.rotate(cp.asnumpy(self.imgBase), cv2.ROTATE_180))
        self.imgBaseDark = cp.array(cv2.rotate(cp.asnumpy(self.imgBaseDark), cv2.ROTATE_180))
        self.fogMask = cp.array(cv2.rotate(cp.asnumpy(self.fogMask), cv2.ROTATE_180))
        self.imgFog = cp.array(cv2.rotate(cp.asnumpy(self.imgFog), cv2.ROTATE_180))

        self.imgViewer = cp.array(cv2.rotate(cp.asnumpy(self.imgViewer), cv2.ROTATE_180))
        self.imgDrawer = cp.array(cv2.rotate(cp.asnumpy(self.imgDrawer), cv2.ROTATE_180))
        self.imgDrawn = cp.array(cv2.rotate(cp.asnumpy(self.imgDrawn), cv2.ROTATE_180))
    