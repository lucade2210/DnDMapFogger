import glob
import cv2
import Functions as f
import numpy as np
import random
import os

#Base variables and array declaration
clickRange = 10
imageScale = 1
shapeList = []
coordinateList = []

#Main Function for the on mouse click event
#Will check and execute what to do on click in the current situation
def click_event(event, x, y, flags, param):
    if event == cv2.EVENT_LBUTTONDOWN:
        global imgBase, imgBaseDark, fogMask, imgFog, imgDrawn, imgViewer, imgDrawer, coordinateList, shapeList

        #If coordinatelist has values, than we already have a starting point
        #So start drawing lines or end the shape if the start position is click again
        if len(coordinateList) >= 1:
            f.drawLine(imgDrawn, x, y, coordinateList)

            #Check if the click coordinates are the same as the start position
            # If so, then we draw the shape in the fogmask and overlay this mask on both the viewer and drawer layers
            if f.checkCoordinatesWithStart(x, y, coordinateList, clickRange):
                f.drawShape(fogMask, coordinateList)
                imgViewer = f.overlayMask(fogMask, imgFog, imgBase)
                imgDrawer = f.overlayMask(fogMask, imgBaseDark, imgBase)
                imgDrawn = imgDrawer.copy()
                cv2.imshow('viewer', imgViewer)
                cv2.imshow('drawer', imgDrawer)
                shapeList.append(coordinateList[:])
                coordinateList.clear()

            #If not clicked on starting position, then just simply show the newly drawn line on the drawer layer
            else:
                cv2.imshow('drawer', imgDrawn)
                coordinateList.append((x, y))

        #This else is reached when it is the first click of a new shape, making the starting position
        else:
            f.drawText(imgDrawn, x, y)
            f.drawDot(imgDrawn, x, y, clickRange)
            cv2.imshow('drawer', imgDrawn)
            coordinateList.append((x, y))
        
if __name__ == '__main__':

    #Open all files in the Maps folder and let the user choose one
    mapNames = []
    fileCounter = 0
    for file in glob.glob("Maps\*"):
        mapNames.append(file)
        print(str(fileCounter) + ": " + str(file)[5:])
        fileCounter = fileCounter + 1
    print("")
    chosenMap = int(input("Choose your map by number + enter: "))

    #ImgOriginal = The unedited original image
    #DimX & DimY are dimensions of the image in pixels
    imgOriginal = cv2.imread(mapNames[chosenMap])
    dimX = int(imgOriginal.shape[1] * imageScale)
    dimY = int(imgOriginal.shape[0] * imageScale)
    dim = (dimX, dimY)

    #ImgBase will be the unedited fallback image when revealing parts of the map
    #ImgBaseDark is the darkend version for the drawer window
    imgBase = cv2.resize(imgOriginal, dim, interpolation = cv2.INTER_AREA)
    imgBaseDark = cv2.add(imgBase.copy(), np.array([-40.0]))

    #FogMask will remember the drawn shapes in a boolean array
    #imgFog will be the fog image that is actually used to overlay the base image
    fogMask = np.zeros((dimY, dimX, 3), np.uint8)
    randomFile = "Fogs\\" + random.choice(os.listdir("Fogs\\"))
    imgFog = cv2.resize(cv2.imread(randomFile), dim, interpolation = cv2.INTER_AREA)

    #imgViewer is the compiled image to show in the viewer window
    #imgdrawer is the compiled image to show in the drawer window
    #imgDrawn is the temporarily compiled image to show in the drawer window when drawing. Only this layer will show the lines
    imgViewer = imgFog.copy()
    imgDrawer = imgBaseDark.copy()
    imgDrawn = imgDrawer.copy()

    #This is how they will be compiled in the f.overlayMask function
    #Viewer -> imgFog (mask=0) : imgBase (mask=1)
    #Drawer -> imgBaseDark (mask=0) : imgBase (mask=1)


    cv2.namedWindow('viewer', cv2.WINDOW_FREERATIO)
    cv2.namedWindow('drawer', cv2.WINDOW_FREERATIO)
    cv2.moveWindow('viewer',1000,500)
    cv2.moveWindow('drawer',-1920 ,0)
    cv2.setWindowProperty('viewer', cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_FULLSCREEN)
    cv2.imshow('viewer', imgViewer)
    cv2.imshow('drawer', imgDrawer)
    cv2.setMouseCallback('drawer', click_event)

    cv2.waitKey(0)
    cv2.destroyAllWindows()

