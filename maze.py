#!/usr/bin/env python3
from ev3dev.ev3 import *
from ev3dev2.motor import LargeMotor, OUTPUT_B, OUTPUT_C, SpeedPercent, MoveTank
from ev3dev2.motor import SpeedDPS, SpeedRPM, SpeedRPS, SpeedDPM
from ev3dev2.sound import Sound
from time import sleep

sound = Sound()
leftMotor = LargeMotor('outB')
rightMotor = LargeMotor('outC')
tank_drive = MoveTank(OUTPUT_B, OUTPUT_C)
colSens = ColorSensor()
color = 15

colSens.mode='COL-REFLECT'

def isWhite():
    return colSens.value() > 15


def debug_print(*args, **kwargs):
    '''Print debug messages to stderr.

    This shows up in the output panel in VS Code.
    '''
    print(*args, **kwargs, file=sys.stderr)

def turnRight():
    tank_drive.on_for_degrees(50, -50, 25)

def turnLeft():
    tank_drive.on_for_degrees(-50, 50, 25)

while not isWhite():
    debug_print(colSens.value())
    tank_drive.run_forever(speed_sp=-150)

sound.speak('White')

while True:

    if isWhite():
        tank_drive.run_forever(speed_sp=-20)
    else:
        foundWhite = False
        for i in range(25):
            turnRight()
            if isWhite():
                foundWhite = True
                break
        if foundWhite:
            continue
        else:
            while not isWhite():
                turnLeft()