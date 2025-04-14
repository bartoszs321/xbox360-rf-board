from picozero import DigitalOutputDevice, DigitalInputDevice
from cmd_list import cmdlist
import time

# xbox_rf.py
#
# A Python library to control Xbox 360 RF Units
# with an Raspberry Pi.
#
# Created by Tino Goehlert -> https://github.com/tinogoehlert/xbox360_rf/blob/master/xbox_rf.py
#
# www.astrorats.org | @_tin0_

data_pin = 17  # data line (pin 6 on the module)
clock_pin = 16  # clock line (pin 7 on module)

data_device = DigitalOutputDevice(data_pin)
clock_device = DigitalInputDevice(clock_pin, pull_up=True)

# Reverse cmdlist. Needed by Bruteforce to resolv
# binary commands to their names.
cmdlist_reversed = dict([(v, k) for k, v in cmdlist.items()])


# SendData
#   Sends a Command to the Module
def SendData(command, delay=0):
    data_device.value = 0

    prev = 1
    for i in range(len(command)):
        # print("prev: " + str(prev))
        while prev == clock_device.value:
            pass
        # print("1 clock_device.value: " + str(clock_device.value))
        prev = clock_device.value
        # print("2 prev: " + str(prev))
        data_device.value = int(command[i])

        while prev == clock_device.value:
            pass
        # print("2 clock_device.value: " + str(clock_device.value))
        prev = clock_device.value
        # print("3 prev: " + str(prev))
    data_device.value = 1
    time.sleep_ms(delay)


# SendInteger
#   Converts an Decimal Value to a command
#   and sends it via SendData
def SendInteger(num):
    if num < 255:
        binstr = "00" + "{0:b}".format(num)
        binstr = "0" * (7 - (len(binstr) - 3)) + binstr
        SendData(binstr)


# Init
#   Start Xbox 360 boot sequence.
def Init():
    SendData(cmdlist["led_cmd"])
    time.sleep_ms(5000)


# BootAnimation
#    Plays Xbox 360 Boot Animation
def BootAnimation():
    SendData(cmdlist["anim_cmd"])
    time.sleep_ms(7000)


# SendCommand
#   sends a command according to its name
def SendCommand(name, delay=0):
    SendData(cmdlist[name], delay)


# Brutefore
#    Brutefoce attack
#    ignore_known to false if you want to trigger
#    commands that are already in cmdlist.
def Bruteforce(begin=0, end=255, ignore_known=True, blocking=False):
    while begin <= end:
        binstr = "00" + "{0:b}".format(begin)
        binstr = "0" * (7 - (len(binstr) - 3)) + binstr
        if blocking:
            input("continue...")
        else:
            time.sleep_ms(1000)
        if binstr not in cmdlist.values() or ignore_known == False:
            SendData(binstr)
            print(binstr + " : " + str(begin))
        else:
            print(binstr + " : " + cmdlist_reversed[binstr])

        begin += 1
