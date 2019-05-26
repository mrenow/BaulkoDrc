import serial
#import time

startMarker = ord('<')
endMarker = ord('>')

rpm = 0
received = ""

ArduinoReady = False

Arduino = serial.Serial(port='COM3', baudrate=9600, timeout=None)


def encode(inStr):
    outStr = ""
    s = len(inStr)

    for n in range(0, s):
        x = ord(inStr[n])
        outStr = outStr + chr(x)

    return (outStr)


def send(message):
    global startMarker, endMarker
    message = encode(message)
    sendcmd = chr(startMarker) + message + chr(endMarker)

    Arduino.write(bytes(sendcmd, 'latin-1'))


def readArduino():
    global received
    x = "z"

    if Arduino.in_waiting > 0:
        received = ""

        while ord(x) != startMarker:
            x = Arduino.read()
            #print("NO START")
            #print(x)

        while ord(x) != endMarker:
            x = Arduino.read()
            if ord(x) != endMarker:
                received = received + chr(ord(x))
            #if ord(x) == endMarker:
            #print(x)
            #print("NO END")
        print(received)



def waitforArduino():
    global ArduinoReady

    readArduino()

    if received == 'Arduino is ready':
        ArduinoReady = True
        print("Go")

        send("START")


def demandRPM():
    send("Pls send RPM")


def get_RPM():
    readArduino()

    return int(received)


while ArduinoReady == False:
    waitforArduino()

while True:
    rpm = get_RPM()
    print(rpm)
