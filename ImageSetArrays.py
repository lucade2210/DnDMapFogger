from pydoc import ispackage
from re import L
import cv2
import numpy as np
import cupy as cp
import os
import random
import Functions as f

class ImageSetArrays:

    def __init__(self, dim, imagePath, imgFog):
        self.counter = 100
        self.dimViewport = dim
        self.dimXViewport = self.dimViewport[0]
        self.dimYViewport = self.dimViewport[1]
        self.clickRange = round(self.dimXViewport / 150)
        
        self.isPannable = "pan" in imagePath
        self.hasNoFog = "noFog" in imagePath
        self.imgOriginal = cv2.imread(imagePath) #OG unedited image
        self.imgFog = imgFog
        
        self.dimYOriginal = self.imgOriginal.shape[0]
        self.dimXOriginal = self.imgOriginal.shape[1]
        self.dimOriginal = (self.dimXOriginal, self.dimYOriginal)
        self.panningCursor = [0,0] #Y,X

        self.coordinateList = []
        self.coordinateListDrawer = []
        self.resetFogPercentile = 100

        if not self.isPannable:
            self.dimYOriginal = self.dimYViewport
            self.dimXOriginal = self.dimXViewport
            self.dimOriginal = self.dimViewport

        self.imgBase = cv2.resize(self.imgOriginal, self.dimOriginal, interpolation = cv2.INTER_AREA) #resized image
        self.imgBaseDark = cv2.add(self.imgBase.copy(), np.array([-40.0])) #darkend image
        self.imgBase = cp.array(self.imgBase)
        self.imgBaseDark = cp.array(self.imgBaseDark)

        self.imgViewer = self.imgFog.copy() #combined image for viewer
        self.imgDrawer = self.imgBaseDark[self.panningCursor[0]:self.panningCursor[0]+self.dimYViewport,self.panningCursor[1]:self.panningCursor[1]+self.dimXViewport,:].copy() #combined image for drawer
        self.imgDrawn = self.imgDrawer.copy() #temp image for drawer with drawn lines

        if self.hasNoFog == True:
            self.fogMask = cp.ones((self.dimYOriginal, self.dimXOriginal, 1), cp.uint8) #masking shape arrays
            self.overlayFogMaskWithViewerVid(imgFog)
        else:
            self.fogMask = cp.zeros((self.dimYOriginal, self.dimXOriginal, 1), cp.uint8) #masking shape arrays
            


        
        #print(self.imgBase.shape)
        #print(self.imgBaseDark.shape)
        #print(self.fogMask.shape)
        #print(self.imgFog.shape)
        #print(self.imgDrawer.shape)

        

    def setPanningCursor(self,direction):
        shift = 100
        if direction == "up":
            self.panningCursor[0] = max(0, min(self.dimYOriginal-self.dimYViewport,self.panningCursor[0]-shift))
        if direction == "down":
            self.panningCursor[0] = max(0, min(self.dimYOriginal-self.dimYViewport,self.panningCursor[0]+shift))
        if direction == "left":
            self.panningCursor[1] = max(0, min(self.dimXOriginal-self.dimXViewport,self.panningCursor[1]-shift))
        if direction == "right":
            self.panningCursor[1] = max(0, min(self.dimXOriginal-self.dimXViewport,self.panningCursor[1]+shift))

        self.overlayImageDrawer()
        self.resetDrawnImage()
        self.updateDrawerImage()

        

    def updateDrawerImage(self):
        cv2.imshow('drawer', cp.asnumpy(self.imgDrawn))

    def updateViewerImage(self):
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
        self.imgViewer = f.overlayMaskWeighted(
            self.fogMask[self.panningCursor[0]:self.panningCursor[0]+self.dimYViewport,self.panningCursor[1]:self.panningCursor[1]+self.dimXViewport,:], 
            imgVid, 
            self.imgBase[self.panningCursor[0]:self.panningCursor[0]+self.dimYViewport,self.panningCursor[1]:self.panningCursor[1]+self.dimXViewport,:]
            ).astype(np.uint8)

    def overlayImageDrawer(self):
        self.imgDrawer = f.overlayMask(
            self.fogMask[self.panningCursor[0]:self.panningCursor[0]+self.dimYViewport,self.panningCursor[1]:self.panningCursor[1]+self.dimXViewport,:],
            self.imgBaseDark[self.panningCursor[0]:self.panningCursor[0]+self.dimYViewport,self.panningCursor[1]:self.panningCursor[1]+self.dimXViewport,:], 
            self.imgBase[self.panningCursor[0]:self.panningCursor[0]+self.dimYViewport,self.panningCursor[1]:self.panningCursor[1]+self.dimXViewport,:]
        )

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

        
    