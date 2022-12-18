import glob
import cv2
import Functions as f
import Controls as c
import numpy as np
import cupy as cp
import time as t
import os

from fileLocations import fileLocations
location = fileLocations.location

from ImageSetArrays import ImageSetArrays

#Base variables and array declaration
clickRange = 10
imageScale = 1
resolutions = (("1080p", (1920,1080)),("1440p", (2560,1440)),("4k", (3840,2160)))
panScaling = 1
chosenResolution = 0
imageSets = []
chosenMapCursor = 0
closingBoolean = False

#MouseCallBack Params
drawingType = 1 # 1  = PolyLine, -1 = Dragging Circle
isDrawing = False
lastPosX = 0
lastPosY = 0


def exitMapFogger():
    cv2.destroyAllWindows()
    exit()

def onMouseCallback(event, x, y, flags, param):
    c.clickPointInDrawer(event, x, y, flags, param)

def setCallback():
    imageSets[chosenMapCursor].reload()
    param = [imageSets[chosenMapCursor], drawingType, isDrawing, lastPosX, lastPosY]
    cv2.setMouseCallback('drawer', onMouseCallback, param)

if __name__ == '__main__':

    #Choose base resolution and set dims
    fileCounter = 0
    for res in resolutions:
        print(str(fileCounter) + " " + str(res))
        fileCounter += 1
    print("")
    chosenResolution = int(input("Choose the resolution of your viewer display (Integer)"))
    dim = resolutions[chosenResolution][1]
    dimString = resolutions[chosenResolution][0]

    #Load Wallpaper image for fog
    imgFog = cp.array(cv2.resize(cv2.imread("Fogs\\DragonHeist.jpg"), dim, interpolation = cv2.INTER_AREA))
    
    #Open all files in the Maps folder
    mapNames = []
    fileCounter = 0
    filesAndFolders = sorted(glob.glob(location, recursive=True))
    print(filesAndFolders)
    files = [f for f in filesAndFolders if not os.path.isdir(f)]
    for file in files:
        mapNames.append(file)
        print(str(fileCounter) + ": " + str(file)[5:])
        imageSets.append(ImageSetArrays(dim, mapNames[fileCounter], imgFog))
        fileCounter += 1

    #Create Viewer window 
    #  shift it to the right to the external monitor
    #  Fullscreen it
    cv2.namedWindow('viewer', cv2.WINDOW_FREERATIO)
    cv2.moveWindow('viewer',3000,200)
    cv2.setWindowProperty('viewer', cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_FULLSCREEN)

    #Create Drawer window
    #  shift it to the top left corner (being your main monitor)
    cv2.namedWindow('drawer', cv2.WINDOW_FREERATIO)
    cv2.moveWindow('drawer',0 ,0)
    
    #Set callback function including map select and callback params set
    setCallback()

    while True:
        k = cv2.waitKey(1)
        if k!=-1:
            if k==27: # esc = closeCommand = True
                exitMapFogger()
            elif k==46: # . = next image
                chosenMapCursor += 1
                if chosenMapCursor == len(imageSets):
                    chosenMapCursor = 0
            elif k==44: # , = previous image
                chosenMapCursor -= 1
                if chosenMapCursor == -1:
                    chosenMapCursor = len(imageSets) - 1
            elif k==47: # / = switchDrawingType
                drawingType *= -1

            elif k==114: # r = rotate 180
                imageSets[chosenMapCursor].rotate()

            elif k==113: # q = fade back to full fog
                imageSets[chosenMapCursor].resetFog()

            elif k==119: # w = up
                imageSets[chosenMapCursor].setPanningCursor("up")

            elif k==115: # s = down
                imageSets[chosenMapCursor].setPanningCursor("down")

            elif k==97: # a = left
                imageSets[chosenMapCursor].setPanningCursor("left")

            elif k==100: # d = right
                imageSets[chosenMapCursor].setPanningCursor("right")

            else: #if key not in register, print it for debug (to know number for new key)
                print(k)
            
            setCallback()
            

    

