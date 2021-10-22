import glob
import cv2
import Functions as f
import numpy as np

clickRange = 8
scaleSize = 0.25
shapeList = []
coordinateList = []
textColor = 255
maskColor = 100

def click_event(event, x, y, flags, param):
    if event == cv2.EVENT_LBUTTONDOWN:
        global img, imgDark, fogMask, drawMask, imgViewer, imgDrawer, imgDrawerTemp, coordinateList, shapeList

        if len(coordinateList) >= 1:
            f.drawLine(imgDrawerTemp, x, y, coordinateList)
        else:
            f.drawText(imgDrawerTemp, x, y)
        
        if f.checkCoordinatesListInRange(x, y, coordinateList, clickRange):
            f.drawShape(fogMask, coordinateList)
            drawMask = np.zeros((dimY, dimX, 3), np.uint8)
            imgViewer = f.overlayMask(fogMask, imgViewer, img, maskColor)
            imgDrawer = f.overlayMaskTransparent(fogMask, img, imgDark)
            imgDrawerTemp = imgDrawer.copy()
            cv2.imshow('viewer', imgViewer)
            cv2.imshow('drawer', imgDrawer)
            shapeList.append(coordinateList[:])
            coordinateList.clear()

        else:
            cv2.imshow('drawer', imgDrawerTemp)
            coordinateList.append((x, y))

if __name__ == '__main__':
    mapNames = []
    fileCounter = 0
    for file in glob.glob("Maps\*"):
        mapNames.append(file)
        print(str(fileCounter) + ": " + str(file)[5:])
    print("")
    chosenMap = int(input("Choose your map by number + enter: "))


    imgOriginal = cv2.imread(mapNames[chosenMap])
    dimX = int(imgOriginal.shape[1] * scaleSize)
    dimY = int(imgOriginal.shape[0] * scaleSize)
    dim = (dimX, dimY)

    img = cv2.resize(imgOriginal, dim, interpolation = cv2.INTER_AREA)
    imgDark = img.copy()
    imgDark = cv2.add(imgDark, np.array([-40.0]))
    
    fogMask = np.full((dimY, dimX, 3), maskColor, np.uint8)
    drawMask = np.zeros((dimY, dimX, 3), np.uint8)
    imgViewer = img.copy()
    imgDrawer = img.copy()
    imgViewer = f.overlayMask(fogMask, imgViewer, img, maskColor)
    imgDrawer = np.where(fogMask == 0, imgDrawer, imgDark)
    imgDrawerTemp = imgDrawer.copy()

    cv2.imshow('viewer', imgViewer)
    cv2.imshow('drawer', imgDrawer)
    cv2.setMouseCallback('drawer', click_event)

    cv2.waitKey(0)
    cv2.destroyAllWindows()
