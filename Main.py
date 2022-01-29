import glob
import cv2
import Functions as f
import Controls as c
import numpy as np
import cupy as cp
import time as t

from fileLocations import fileLocations
location = fileLocations.locationLaptop

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
    
    #Open all files in the Maps folder and let the user choose one
    mapNames = []
    fileCounter = 0
    for file in glob.glob(location):
        mapNames.append(file)
        print(str(fileCounter) + ": " + str(file)[5:])
        imageSets.append(ImageSetArrays(dim, mapNames[fileCounter]))
        fileCounter += 1


    cv2.namedWindow('viewer', cv2.WINDOW_FREERATIO)
    cv2.namedWindow('drawer', cv2.WINDOW_FREERATIO)
    cv2.moveWindow('viewer',3000,200)
    cv2.moveWindow('drawer',0 ,0)
    cv2.setWindowProperty('viewer', cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_FULLSCREEN)

    imageSets[chosenMapCursor].reload()
    param = [imageSets[chosenMapCursor], drawingType, isDrawing, lastPosX, lastPosY]
    cv2.setMouseCallback('drawer', c.clickPointInDrawer, param)


    while True:

        video = cv2.VideoCapture("VideoOverlays\smoke02-" + dimString + ".mp4")
        closingBoolean = False

        while True:
            startTime = t.time() * 1000
            ret, imgVid = video.read()
            if ret == True:
                
                imgVid = cp.array(imgVid)
                
                imageSets[chosenMapCursor].overlayFogMaskWithViewerVid(imgVid)
                imageSets[chosenMapCursor].updateViewerImage()

                k = cv2.waitKey(1)

                if k!=-1:
                    if k==27: # esc = closeCommand = True
                        closingBoolean = True
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

                    else:
                        print(k)
                    
                    imageSets[chosenMapCursor].reload()
                    param = [imageSets[chosenMapCursor], drawingType, isDrawing, lastPosX, lastPosY]
                    cv2.setMouseCallback('drawer', c.clickPointInDrawer, param)

                
                if closingBoolean == True:
                    break
                
            else:
                break
            #print(t.time()*1000 - startTime)
        
        if closingBoolean == True:
            break

    video.release()
    cv2.destroyAllWindows()
    exit()

