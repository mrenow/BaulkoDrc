import serial

steer_channel = 0
drive_channel = 1

steer_min = 1000
steer_max = 11000
drive_min = 1000
drive_max = 11000

maestro = serial.Serial(port='COM17')


def close_maestro():
    maestro.close()


def set_target(channel, target):
    if channel == steer_channel:
        if target < steer_min:
            target = steer_min
        if target > steer_max:
            target = steer_max
    if channel == drive_channel:
        if target < drive_min:
            target = drive_min
        if target > drive_max:
            target = drive_max

    lower = target & 0x7f
    upper = (target >> 7) & 0x7f
    command = chr(0x84) + chr(channel) + chr(lower) + chr(upper)

    maestro.write(bytes(command, 'latin-1'))


if __name__ == "__main__":

    set_target(drive_channel, 6000)
    set_target(steer_channel, 6000)


