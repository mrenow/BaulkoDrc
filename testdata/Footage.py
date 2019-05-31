import cv2 as cv




if __name__ == "__main__":

    cap = cv.VideoCapture(1)
    record = cv.VideoWriter("MCIC3.avi",cv.VideoWriter_fourcc(*'XVID'),25,(640,480))
    time = 0
    cv.namedWindow("capture")

    while(True):
        retval,frame = cap.read()
        if(not retval):continue
        record.write(frame)
        cv.imshow("capture",frame)
        cv.waitKey(1)
    record.release()
    cap.release()
