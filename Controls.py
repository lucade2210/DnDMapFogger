import cv2
import Functions as f

def exitFunction():
    cv2.destroyAllWindows()
    exit()

#drawingType from param--> 1  = PolyLine, -1 = Dragging Circle

def clickPointInDrawer(event, x, y, flags, param):
    imageSetArray = param[0]
    drawingType = param[1]
    isDrawing = param[2]

    if event == cv2.EVENT_LBUTTONDOWN:

        if drawingType == 1:

            isDrawing = False

            #If coordinatelist has values, than we already have a starting point
            #So start drawing lines or end the shape if the start position is click again
            if len(imageSetArray.coordinateList) >= 1:
                imageSetArray.imgDrawn = f.drawLine(imageSetArray.imgDrawn, x, y, imageSetArray.coordinateList)

                #Check if the click coordinates are the same as the start position
                # If so, then we draw the shape in the fogmask and overlay this mask on both the viewer and drawer layers
                if f.checkCoordinatesWithStart(x, y, imageSetArray.coordinateList, imageSetArray.clickRange):
                    imageSetArray.fogMask = f.drawShape(imageSetArray.fogMask, imageSetArray.coordinateList)
                    imageSetArray.imgDrawer = f.overlayMask(imageSetArray.fogMask, imageSetArray.imgBaseDark, imageSetArray.imgBase)
                    imageSetArray.resetDrawnImage()
                    imageSetArray.updateDrawerImage()
                    imageSetArray.updateViewerImage()
                    imageSetArray.coordinateList.clear()

                #If not clicked on starting position, then just simply show the newly drawn line on the drawer layer
                else:
                    imageSetArray.updateDrawerImage()
                    imageSetArray.coordinateList.append((x, y))

            #This else is reached when it is the first click of a new shape, making the starting position
            else:
                imageSetArray.imgDrawn = f.drawText(imageSetArray.imgDrawn, x, y)
                imageSetArray.imgDrawn = f.drawDot(imageSetArray.imgDrawn, x, y, imageSetArray.clickRange)
                imageSetArray.updateDrawerImage()
                imageSetArray.coordinateList.append((x, y))
        
        elif drawingType == -1:
            isDrawing = True
            param[2] = True
            imageSetArray.fogMask = f.drawDot(imageSetArray.fogMask, x, y, imageSetArray.clickRange*5)
            imageSetArray.imgDrawer = f.overlayMask(imageSetArray.fogMask, imageSetArray.imgBaseDark, imageSetArray.imgBase)
            imageSetArray.resetDrawnImage()
            imageSetArray.updateDrawerImage()
            imageSetArray.updateViewerImage()

    if event == cv2.EVENT_MOUSEMOVE:
        if isDrawing == True:
            imageSetArray.fogMask = f.drawDot(imageSetArray.fogMask, x, y, imageSetArray.clickRange*5)
            imageSetArray.imgDrawer = f.overlayMask(imageSetArray.fogMask, imageSetArray.imgBaseDark, imageSetArray.imgBase)
            imageSetArray.resetDrawnImage()
            imageSetArray.updateDrawerImage()
            #imageSetArray.updateViewerImage()

    if event == cv2.EVENT_LBUTTONUP:
        isDrawing = False
        param[2] = False

