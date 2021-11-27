import cv2
import numpy as np
import cupy as cp
import os
import random
import Functions as f

class ImageSetArrays:

    def __init__(self, dim, imagePath):
        self.counter = 100
        self.dim = dim
        self.dimX = dim[0]
        self.dimY = dim[1]
        self.clickRange = round(self.dimX / 150)

        self.imgOriginal = cv2.imread(imagePath) #OG unedited image
        self.imgBase = cv2.resize(self.imgOriginal, dim, interpolation = cv2.INTER_AREA) #resized image
        self.imgBaseDark = cv2.add(self.imgBase.copy(), np.array([-40.0])) #darkend image
        self.imgBase = cp.array(self.imgBase)
        self.imgBaseDark = cp.array(self.imgBaseDark)

        self.fogMask = cp.zeros((self.dimY, self.dimX, 1), cp.uint8) #masking shape arrays
        randomFile = "Fogs\\" + random.choice(os.listdir("Fogs\\"))
        self.imgFog = cp.array(cv2.resize(cv2.imread(randomFile), dim, interpolation = cv2.INTER_AREA)) #fog image


        self.imgViewer = self.imgFog.copy() #combined image for viewer
        self.imgDrawer = self.imgBaseDark.copy() #combined image for drawer
        self.imgDrawn = self.imgDrawer.copy() #temp image for drawer with drawn lines

        self.coordinateList = []
        self.resetFogPercentile = 100

    def updateDrawerImage(self):
        cv2.imshow('drawer', cp.asnumpy(self.imgDrawn))

    def updateViewerImage(self):
        self.imgViewer[5,1250:1260,0] = 255
        cv2.imshow('viewer', cp.asnumpy(self.imgViewer))
        if self.counter == 100:
            self.counter = 0
        self.counter += 2

    def overlayFogMaskWithViewerVid(self, imgVid):
        if self.resetFogPercentile != 100:
            self.fogMask = cp.where(self.fogMask, self.resetFogPercentile / 100, 0)
            self.resetFogPercentile -= 1
            if self.resetFogPercentile == 0:
                self.resetFogPercentile = 100
        self.imgViewer = f.overlayMaskWeighted(self.fogMask, imgVid, self.imgBase).astype(np.uint8)

    def resetDrawnImage(self):
        self.imgDrawn = self.imgDrawer.copy()
    
    def reload(self):
        self.coordinateList.clear()
        self.resetDrawnImage()
        self.updateDrawerImage()
        self.updateViewerImage()
    
    def rotate(self):
        self.imgOriginal = cv2.rotate(self.imgOriginal, cv2.ROTATE_180)
        self.imgBase = cp.array(cv2.rotate(cp.asnumpy(self.imgBase), cv2.ROTATE_180))
        self.imgBaseDark = cp.array(cv2.rotate(cp.asnumpy(self.imgBaseDark), cv2.ROTATE_180))
        self.fogMask = cp.rot90(self.fogMask,2)
        self.imgFog = cp.array(cv2.rotate(cp.asnumpy(self.imgFog), cv2.ROTATE_180))

        self.imgViewer = cp.array(cv2.rotate(cp.asnumpy(self.imgViewer), cv2.ROTATE_180))
        self.imgDrawer = cp.array(cv2.rotate(cp.asnumpy(self.imgDrawer), cv2.ROTATE_180))
        self.imgDrawn = cp.array(cv2.rotate(cp.asnumpy(self.imgDrawn), cv2.ROTATE_180))

    def resetFog(self):
        print("reset")
        print(self.fogMask[100,100,0])
        self.resetFogPercentile = 99
        
    