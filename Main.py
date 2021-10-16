import cv2
import Functions as f

range = 8
scale = 0.25
shapeList = []
coordinateList = []

def click_event(event, x, y, flags, param):
    if event == cv2.EVENT_LBUTTONDOWN:
        global img
        global imgMasked
        global coordinateList
        global shapeList

        if len(coordinateList) >= 1:
            f.drawLine(mask, x, y, coordinateList)
        else:
            f.drawText(mask, x, y)
        
        if f.checkCoordinatesListInRange(x, y, coordinateList, range):
            f.drawShape(mask, coordinateList)
            imgMasked = cv2.addWeighted(img, 0.4, mask, 0,1, 0)
            cv2.imshow('image', imgMasked)
            shapeList.append(coordinateList[:])
            coordinateList.clear()
            print('Shapes: ' + str(shapeList))
            print('')

        else:
            cv2.imshow('image', imgMasked)
            coordinateList.append((x, y))
            print('')



imgOriginal = cv2.imread('Map Cragmaw Cave.jpg')
maskOriginal = cv2.imread('TransparentMask.png')

dim = (int(imgOriginal.shape[1] * scale), int(imgOriginal.shape[0] * scale))

img = cv2.resize(imgOriginal, dim, interpolation = cv2.INTER_AREA)
mask = cv2.resize(maskOriginal, dim, interpolation = cv2.INTER_AREA)
imgMasked = cv2.addWeighted(img, 1, mask, 1, 0)



cv2.imshow('image', imgMasked)

cv2.setMouseCallback('image', click_event)

cv2.waitKey(0)
cv2.destroyAllWindows()

