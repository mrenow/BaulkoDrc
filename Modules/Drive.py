from .Objects import findObjects
from .Maestro import *
import cv2 as cv
import numpy as np

# from PSEye

resolution = (640,480)

#gets x co ordinate of screen target
def getScreenTarget(objects:dict):
    objects = sorted(sum(objects.values(), []))
    # gap, location
    maxgap = (0,0)
    for o1,o2 in zip(objects[1:],objects[:-1]):
        gap = o2[1]-o1[1]
        if(gap > maxgap[1]-maxgap[0]):
            maxgap = (o1,o2)
    return (maxgap[0]+maxgap[1])/2



#TURN_COEFF = 1
SPEED_COEFF = 100
def driveToTarget(targetx):
    screenradius = resolution[0]//2
    turn = np.interp(targetx, (-screenradius,screenradius), (-100,100))
    speed = max(10, SPEED_COEFF//turn)
    drive(speed,turn)







if __name__ ==  "__main__":
    device = 1
    camera = cv.VideoCapture(device)
    while(True):
        retval,frame = camera.read()
        if(not retval): continue
        objects = findObjects()
        target = getScreenTarget(objects)
    driveToTarget(target)

