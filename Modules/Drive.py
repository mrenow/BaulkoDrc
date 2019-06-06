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
    drive(0,turn)







if __name__ ==  "__main__":

    clear()
    time.sleep(5)
    device1 = 0
    device2 = 1
    record = cv.VideoWriter("whee.avi",cv.VideoWriter_fourcc(*'XVID'),25,(640,480))

    # Video setup
    camera1 = cv.VideoCapture(device1)
    camera2 = cv.VideoCapture(device2)
    # 3 is width, 4 is height
    resolution1 = (int(camera1.get(3)), int(camera1.get(4)))
    resolution2 = (int(camera2.get(3)), int(camera2.get(4)))
    assert(resolution1[1] == resolution2[1])
    frame = np.zeros( (resolution1[1],(resolution1[0] + resolution2[0]),3), dtype = np.uint8)
    while(True):
        retval1,frame1 = camera1.read()
        retval2,frame2 = camera2.read()
        if(not retval1 or not retval2): continue
        frame[:,:resolution1[0]] = frame1
        frame[:,resolution1[0]:] = frame2

        # Vision and Pathing
        objects = getObjects(frame)
        target = getScreenTarget(objects)
        driveToTarget(target)
        record.write(frame)
        if cv.waitKey(25) & 0xFF == ord(' '):
            record.release()
            break