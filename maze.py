#!/usr/bin/env python3
from ev3dev.ev3 import *
from ev3dev2.motor import LargeMotor, OUTPUT_B, OUTPUT_C, SpeedPercent, MoveTank
from ev3dev2.motor import SpeedDPS, SpeedRPM, SpeedRPS, SpeedDPM, MoveDifferential
from ev3dev2.sound import Sound
from time import sleep

sound = Sound()
leftMotor = LargeMotor('outB')
rightMotor = LargeMotor('outC')
tank_drive = MoveTank(OUTPUT_B, OUTPUT_C)
colSens = ColorSensor()
color = 15

colSens.mode='COL-REFLECT'

def robotSeesWhite():
    return colSens.value() > 15

def robotSeesYellow();
    return colSens.value() > 30

def debug_print(*args, **kwargs):
    '''Print debug messages to stderr.

    This shows up in the output panel in VS Code.
    '''
    print(*args, **kwargs, file=sys.stderr)

def turnRight():
    tank_drive.on_for_degrees(100, -100, 25)

def turnLeft():
    tank_drive.on_for_degrees(-100, 100, 25)



# Etsitään valkoinen viiva
while not robotSeesWhite():
    debug_print(colSens.value())
    tank_drive.run_forever(speed_sp=-150)

sound.speak('White')

# Kuljetaan viivaa pitkin
while True:

    # Ajetaan suoraan, jos ollaan viivan päällä
    if robotSeesWhite():
        tank_drive.run_forever(speed_sp=-200)
    # Ajetaan 200mm suoraan, jos ollaan keltaisen päällä
    # Odotetaan 10s ja käännytään 170 astetta vasempaan
    elif robotSeesYellow():
        mdiff.on_for_distance(SpeedRPM(60), 200)
        time.sleep(10)
        mdiff.turn_left(SpeedRPM(40), 170)
    else:
        whiteColorFound = False

        # Etsitään käännöstä oikealle max 90 astetta
        for i in range(20):
            turnRight()
            if robotSeesWhite():
                whiteColorFound = True
                break
        if whiteColorFound:
            # Jatketaan viivaa pitkin
            turnRight()
            continue
        else:
            # Etsitään valkoinen vasemmalta
            while not robotSeesWhite():
                turnLeft()
            # Valkoinen löytyi, suoristetaan viivan suuntaisesti
            turnLeft()
            turnLeft()

