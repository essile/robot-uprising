#!/usr/bin/env python3
from ev3dev.ev3 import *
from ev3dev2.motor import LargeMotor, OUTPUT_B, OUTPUT_C, SpeedRPM, MoveDifferential, MoveTank
from ev3dev2.wheel import EV3Tire
from time import sleep

leftMotor = LargeMotor('outB')
rightMotor = LargeMotor('outC')
tank_drive = MoveTank(OUTPUT_B, OUTPUT_C)

# Arvoja pituuden mittaamista varten
STUD_MM = 8
mdiff = MoveDifferential(OUTPUT_B, OUTPUT_C, EV3Tire, 16 * STUD_MM)

def runStraight(speed, distanceMM):
    mdiff.on_for_distance(SpeedRPM(speed), distanceMM)




# Aja suoraan pitkä 240
runStraight(-100, 240)


## MUTKA LÄHDÖSTÄ

tank_drive.on_for_degrees(-100, 100, 450) #vasen käännös 450, suora 710

## SUORA
runStraight(-100, 710)

## EKA KULMA

tank_drive.on_for_degrees(100, -100, 450) # Oikea käännös
runStraight(-100, 400)

## TOKA KULMA
tank_drive.on_for_degrees(100, -100, 380) # Oikea käännös

## PITKÄ VÄLISUORA
runStraight(-100, 650)

## TIUKKA MUTKA

tank_drive.on_for_degrees(-100, 100, 630)
runStraight(-100, 660)

## KULMA KOHTI MAALIA
tank_drive.on_for_degrees(100, -100, 540) # Oikea käännös


runStraight(-100, 550)
tank_drive.on_for_degrees(-100, 100, 300)


## VIKA SUORA
runStraight(-100, 350)