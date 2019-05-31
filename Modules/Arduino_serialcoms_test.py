import serial

startMarker = ord('<')
endMarker = ord('>')

ArduinoReady = False
TEST = True

Arduino = serial.Serial(port='COM3', baudrate=9600)

def waitforArduino():
    global ArduinoReady

    if readArduino() == '<Arduino is ready>':
        ArduinoReady = True
        print("Go")


def readArduino():
    global startMarker, endMarker
    x = "z"
    y = ""

    while ord(x) != startMarker:
        x = Arduino.read()
        #print("NO START")
        #print(x)

    while ord(x) != endMarker:
        y = y + chr(ord(x))
        x = Arduino.read()
        #print(x)
        # print(y)
        #print("NO END")

    y = y + chr(ord(x))

    print(y)
    # print(x)

    return y


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


waitforArduino()

if ArduinoReady == True:

    send('START')

    while TEST == True:
        data = readArduino()

        print("loop")
        print(data)
