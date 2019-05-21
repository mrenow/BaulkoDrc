import numpy as np
import cv2 as cv


'''
Contains getObjects()

Input is raw image data

Output is a tuple of centre and radii in x and y directions.
Should be sufficient for Daniel Pathing. 

'''
#Maybe use an adpativeish thresh?
def toMask(image:np.ndarray, lower, upper, format = cv.COLOR_BGR2HSV, noise = 5, debug = False):
    #assert image.dtype == type(upper)
    #assert image.dtype == type(lower)
    #image = cv.adaptiveThreshold(image,255,cv.ADAPTIVE_THRESH_GAUSSIAN_C,cv.THRESH_BINARY,)

    image = cv.cvtColor(image, format)
    image = cv.inRange(image, lower, upper)

    # Kernel shape accounts for how perspective squishes objects.
    image = cv.morphologyEx(image, cv.MORPH_OPEN, np.ones((noise,noise//2)))

    image = cv.morphologyEx(image, cv.MORPH_CLOSE,np.ones((8*noise,4*noise)))
    if (debug):
        cv.namedWindow("tomask")
        cv.imshow("tomask", image)

    return image

# Assumes noiseless
# Uses canny and contour detection to only return large onscreen objects.
# Issues: Usually returns duplicates of objects. Can fix by using a Open-only gradient operation,
# but this becomes unreliable in yellow line detection.
def findObjects(image:np.ndarray, threshlow, minwidth, minheight = None, frame = None, debug = None) -> list:

    if(not debug is None):
        cv.namedWindow("findObjects")

    if(not minheight):
        minheight = minwidth

    # Add a border of zeros around image so that edges are also detected at edge of the image.
    borderedimage = np.zeros((image.shape[0] + 2, image.shape[1] + 2), dtype=np.uint8)
    borderedimage[1:-1, 1:-1] = image

    # Extracts edges and then produces contours joining edge pixels.
    # edges = cv.morphologyEx(borderedimage, cv.MORPH_OPEN, np.ones((2,2)))-borderedimage
    edges = cv.morphologyEx(borderedimage, cv.MORPH_GRADIENT, np.ones((2,2)))
    contours, _ = cv.findContours(edges, cv.RETR_TREE, cv.CHAIN_APPROX_SIMPLE)

    if (not debug is None): cv.drawContours(debug,contours,-1,(255,0,0))

    # List of tuples : (x,y,rx,ry)
    objects = []

    for cont in contours:
        # Get polygonal approximation, a list of points/
        poly = cv.approxPolyDP(cont, epsilon = 5, closed = True)

        # get bounding boxes around polys. Shift all elements by -1.
        box = list(map(lambda x: int(x-1), cv.boundingRect(poly)))

        # Unpack
        width = box[2]
        height = box[3]
        x,y = (box[0]+box[2]//2, box[1]+box[3]//2)

        # Do not include if object is too small.
        if(width >= minwidth and height >= minheight):
            objects.append((x,y,width//2,height//2))

            if(not debug is None): cv.rectangle(debug, (box[0], box[1]), (box[0]+box[2], box[1]+box[3]), (0, 0, 255))

    return objects








'''
# input greyscale uint8 image. Should output one contour.
def getLine(image:np.ndarray, thresh = 128, noise = 3, debug = False):
    assert image.dtype == np.uint8
    assert len(image.shape) == 2
    print(image.shape)
    # Threshold
   # image = cv.adaptiveThreshold(image, maxValue = 255,adaptiveMethod = cv.ADAPTIVE_THRESH_GAUSSIAN_C, thresholdType=cv.THRESH_BINARY,blockSize=33,C=1.5)
    # Noise removal

    if(debug):
        cv.imshow("debug2",image)
        print("getLine->thresh")

    image = cv.morphologyEx(image, cv.MORPH_CLOSE,np.ones((noise,noise//3)))
    image = cv.morphologyEx(image, cv.MORPH_OPEN, np.ones((noise,noise//3)))

    if(debug):
        cv.imshow("debug3",cv.Canny(image,128,256))
        print("getLine->image")
        #cv.waitKey()
'''



def _testInput(name ='0'):
    assert type(name) == str
    if(name.isnumeric()):
        return cv.VideoCapture(int(name))
    if(name[-4:] == ".avi"):
        print("asdfasdf")
        return cv.VideoCapture(name)
    else:
        img:np.ndarray = cv.imread(name)
        assert img.data != None
        # Returns an object that
        return type('',(),dict(img = img, read = lambda self: (True,self.img),isOpened = lambda self:True,open = lambda:None))()

bluelower = (58,100,0)
blueupper = (118,255,255)
yellowlower = (15,66,66)
yellowupper = (66,200,255)
purplelower = (150,20,20)
purpleupper = (200,200,200)
redlower = (0,100,0)
redupper = (15,255,255)


# Returns the centres and dimensions of all objects in a dictionary
def getObjects(frame):
    detection = frame.copy()
    purplechannel = toMask(frame, purplelower,purpleupper,noise = 40, debug = False)
    obstacles = findObjects(purplechannel,60,60,frame = frame, debug = detection)

    bluechannel = toMask(frame, bluelower, blueupper, noise = 5, debug = True)
    blueline = findObjects(bluechannel, 10, 100, 20, frame = frame, debug = detection)

    yellowchannel = toMask(frame, yellowlower, yellowupper, noise = 5, debug = False)
    yellowline = findObjects(yellowchannel, 10, 100, 20, frame = frame, debug = detection)

    redchannel = toMask(frame, redlower,redupper, noise = 20, debug = False)
    cars = findObjects(redchannel, 10, 20, 20, frame = frame, debug = detection)
    if(not detection is None):
        cv.imshow("findObjects",detection)
    return dict(yellowline = yellowline, blueline = blueline, obstacles = obstacles, cars = cars)

if __name__ == "__main__":
    name = "../testdata/TrackTest2.avi"
    #name = "1"
    imgdata:cv.VideoCapture = _testInput(name)
    cv.waitKey(1)
    while(imgdata.isOpened()):
        cv.waitKey(1)

        ret, frame = imgdata.read()
        if(not ret): continue

        obs = getObjects(frame)

        for key in obs.keys():
            if(obs[key]):
                print(key,":",obs[key])










