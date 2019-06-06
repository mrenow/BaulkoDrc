from BaulkoDrc.Modules.Objects import getObjects
from BaulkoDrc.Modules.Maestro import *
import cv2 as cv
import numpy as np

# from PSEye

resolution = (1280//2,480)

#gets x co ordinate of screen target
def getScreenTarget(objects:dict):
    allobjects = []

    if(not objects["blueline"]):
        allobjects.append(0)
    if(not objects["yellowline"]):
        allobjects.append(resolution[0])

    allobjects = sorted(sum(([i[0] for i in o] for o in objects.values() if o), allobjects))
    # gap, location
    maxgap = (0,0)
    print("bounds: ",allobjects)
    for o1,o2 in zip(allobjects[1:],allobjects[:-1]):
        gap = o1-o2
        if(gap > maxgap[0]-maxgap[1]):
            maxgap = (o1,o2)
    print("maxgap: ", maxgap)
    return (maxgap[0]+maxgap[1])/2



#TURN_COEFF = 1

MIN_SPEED = 20
MAX_SPEED = 28

def driveToTarget(targetx):
    turn = 2*np.interp(targetx, [0,resolution[0]], [-100,100])
    turn = max(-100,min(100,turn))
    print("Target: ", targetx)
    speed = interp(1/(turn+1),[1/101,1],[MIN_SPEED,MAX_SPEED])
    drive(speed,turn)







if __name__ ==  "__main__":

    clear()
    time.sleep(5)
    device = 0
    record = cv.VideoWriter("whee.avi",cv.VideoWriter_fourcc(*'XVID'),25,(640,480))
    camera = cv.VideoCapture(device)
    while(True):
        retval,frame = camera.read()
        if(not retval): continue
        objects = getObjects(frame)
        target = getScreenTarget(objects)
        driveToTarget(target)
        record.write(frame)
        cv.waitKey(1)