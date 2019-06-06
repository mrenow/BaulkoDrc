from BaulkoDrc.Modules.Objects import getObjects
from BaulkoDrc.Modules.Maestro import *
import cv2 as cv
import numpy as np
import keyboard

# from PSEye

resolution = (1280//2,480)


def takeX(elem):
    return elem[1][0]


#gets x co ordinate of screen target
def getScreenTarget(objects:dict):
    #allobjects = []
    # Dealing with cases where one line isn't being seen by the cameras
    if(not objects["blueline"]):
        #allobjects.append(0)
        objects.update(leftwall = 0)
    if(not objects["yellowline"]):
        #allobjects.append(resolution[0])
        objects.update(rightwall = resolution[0])

    #allobjects = sorted(sum(([i[0] for i in o] for o in objects.values() if o), allobjects))
    newobjects = sum([[(key,el) for el in objects[key]] for key in objects.keys()], [])
    newobjects.sort(key=takeX)

    # gap, location
    maxgap = (0,0)
    print("bounds: ", objects)

    #s2 will be larger than t2
    for (s1, s2), (t1, t2) in zip(newobjects[1:], newobjects[:-1]):
        viable = True
        gap = s2[0] - t2[0]

        if (s1 == "yellowline" and t1 == "yellowline") or (s1 == "blueline" and t1 == "blueline"):
            viable = False

        if(gap > maxgap[0]-maxgap[1] and viable == True):
            maxgap = (s2, t2)

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
            clear()
            break

        if keyboard.is_pressed('w'):
            MAX_SPEED += 1
            time.sleep(0.2)
        if keyboard.is_pressed('s'):
            MAX_SPEED -= 1
            time.sleep(0.2)
