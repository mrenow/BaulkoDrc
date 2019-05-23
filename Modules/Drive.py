from BaulkoDrc.Modules.Objects import getObjects
from BaulkoDrc.Modules.Maestro import *
import cv2 as cv
import numpy as np

# from PSEye

resolution = (1280,480)

#gets x co ordinate of screen target
def getScreenTarget(objects:dict):
    objects = sorted(sum(([i[0] for i in o] for o in objects.values() if o), [0,resolution[0]]))
    # gap, location
    maxgap = (0,0)
    print("bounds: ",objects)
    for o1,o2 in zip(objects[1:],objects[:-1]):
        gap = o1-o2
        if(gap > maxgap[0]-maxgap[1]):
            maxgap = (o1,o2)

    return (maxgap[0]+maxgap[1])/2



#TURN_COEFF = 1

MIN_SPEED = 11
MAX_SPEED = 20

def driveToTarget(targetx):
    turn = np.interp(targetx, [0,resolution[0]], [-100,100])
    print("Target: ", targetx)
    speed = interp(1/(turn+1),[1/101,1],[MIN_SPEED,MAX_SPEED])
    drive(speed,turn)







if __name__ ==  "__main__":

    clear()
    time.sleep(5)
    device = "../testdata/TrackTest2.avi"
    camera = cv.VideoCapture(device)
    while(True):
        retval,frame = camera.read()
        if(not retval): continue
        objects = getObjects(frame)
        target = getScreenTarget(objects)
        driveToTarget(target)
        cv.waitKey(1)