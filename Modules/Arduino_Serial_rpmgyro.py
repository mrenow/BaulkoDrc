import serial
#import time

startMarker = ord('<')
endMarker = ord('>')
rpsMarker = ord('@')
yawangleMarker = ord('#')
yawvelocityMarker = ord('$')

received = ""
rps = ""
yawAngle = ""
yawVelocity = ""

ArduinoReady = False
notspam = False

Arduino = serial.Serial(port='COM3', baudrate=38400, timeout=None)


def encode(inStr):
    outStr = ""
    s = len(inStr)

    for n in range(0, s):
        x = ord(inStr[n])
        outStr = outStr + chr(x)

    return (outStr)


def send(message):
    message = encode(message)
    sendcmd = chr(startMarker) + message + chr(endMarker)

    Arduino.write(bytes(sendcmd, 'latin-1'))


def readArduino():
    global received, rps, yawAngle, yawVelocity, notspam
    x = "z"

    if Arduino.in_waiting > 0:
        #print("READING")

        '''if ord(x) == startMarker:
            notspam = True
            print("START")
        else:
            x = Arduino.read()
            print("NO START")
            #print(x)'''

        while ord(x) != startMarker:
            x = Arduino.read()
            #print("NO START")

        while ord(x) != endMarker: #and notspam == True:
            x = Arduino.read()
            #print("RECEIVING")

            if ord(x) == rpsMarker:
                rps = ""
                while ord(x) != endMarker:
                    x = Arduino.read()
                    if ord(x) != endMarker:
                        rps = rps + chr(ord(x))
            elif ord(x) == yawangleMarker:
                yawAngle = ""
                while ord(x) != endMarker:
                    x = Arduino.read()
                    if ord(x) != endMarker:
                        yawAngle = yawAngle + chr(ord(x))
            elif ord(x) == yawvelocityMarker:
                yawVelocity = ""
                while ord(x) != endMarker:
                    x = Arduino.read()
                    if ord(x) != endMarker:
                        yawVelocity = yawVelocity + chr(ord(x))
            else:
                received = ""
                while ord(x) != endMarker:
                    if ord(x) != endMarker:
                        received = received + chr(ord(x))
                    x = Arduino.read()

        #notspam = False


def waitforArduino():
    global ArduinoReady

    readArduino()

    if received == 'Arduino is ready':
        ArduinoReady = True
        print("Go")

        send("START")






while ArduinoReady == False:
    waitforArduino()

while True:
    readArduino()

    print("RPS", rps, sep=": ")
    print("Yaw Angle", yawAngle, sep=": ")
    print("Yaw Velocity", yawVelocity, sep=": ")
    print("Received", received, sep=": ")
