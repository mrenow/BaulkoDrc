import serial
from numpy import interp
import time

maestro = serial.Serial(port='/dev/ttyACM0')

previous_speed = 1


def open_maestro():
    maestro.open()


def close_maestro():
    maestro.close()


class Channel:

    def __init__ (self, channel):
        self.channel = channel
        self.min = 0
        self.max = 0

    def set_range(self, min, max):
        self.min = min
        self.max = max

    def set_target(self, target):
        if target < self.min:
            target = self.min
        if target > self.max:
            target = self.max

        lower = target & 0x7f
        upper = (target >> 7) & 0x7f
        command = chr(0x84) + chr(self.channel) + chr(lower) + chr(upper)

        maestro.write(bytes(command, 'latin-1'))
        #print(bytes(command, 'latin-1'))

    def set_speed(self, target):
        lower = target & 0x7f
        upper = (target >> 7) & 0x7f
        command = chr(0x87) + chr(self.channel) + chr(lower) + chr(upper)

        maestro.write(bytes(command, 'latin-1'))

    def set_accel(self, target):
        lower = target & 0x7f
        upper = (target >> 7) & 0x7f
        command = chr(0x89) + chr(self.channel) + chr(lower) + chr(upper)

        maestro.write(bytes(command, 'latin-1'))

    def min(self):
        return self.min

    def max(self):
        return self.max


def drive(drive_desu, steer_desu):
    global previous_speed

    steer.set_target(int(interp(-steer_desu, [-100, 100], [steer.min, steer.max])))

    if drive_desu < 0 and previous_speed > 0:
        speed.set_target(5999)
        speed.set_target(6001)
        speed.set_target(int(interp(drive_desu, [-100, 100], [speed.min, speed.max])))
    else:
        speed.set_target(int(interp(drive_desu, [-100, 100], [speed.min, speed.max])))

    previous_speed = int(interp(drive_desu, [-100, 100], [speed.min, speed.max]))

    previous_speed = drive_desu
    print("SPEED: {}, STEER: {}".format(drive_desu,steer_desu))


def stop():
    #speed.set_speed(50)
    #speed.set_accel(10)
    speed.set_target(3000)
    #time.sleep(1)
    #speed.set_speed(0)
    #speed.set_accel(0)
def clear():
    drive(0,0)

steer = Channel(0)
speed = Channel(1)

steer.set_range(3000, 9000)
speed.set_range(3000, 9000)

steer.set_speed(10)
steer.set_accel(10)

if __name__ == "__main__":

    drive(20, 40)
    time.sleep(2)
    stop()
