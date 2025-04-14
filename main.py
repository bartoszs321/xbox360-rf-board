import xbox_rf
from picozero import Button, DigitalInputDevice
from time import sleep

# GPIO 16 & 17 used for xbox rf data & clock
sync_button = Button(18, bounce_time=2)  # GPIO18
pwr_ok = DigitalInputDevice(19, bounce_time=5)  # GPIO19


def start_sync_process():
    # print("syncing")
    xbox_rf.SendCommand("ctl_sync", 10000)
    # do something with lights


def turn_off():
    xbox_rf.SendCommand("ctl_shutdown")
    xbox_rf.SendCommand("off", 1000)
    # turn off LEDs somehow


def turn_on():
    # Initialise RF module
    xbox_rf.Init()
    xbox_rf.SendCommand("green_all")


# Setup controller sync button
sync_button.when_pressed = start_sync_process

# Setup pwr on and off callbacks
pwr_ok.when_activated = turn_on
pwr_ok.when_deactivated = turn_off
