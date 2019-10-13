#!/usr/bin/env python3
from ev3dev.ev3 import *
from ev3dev2.motor import 
    LargeMotor, OUTPUT_B, OUTPUT_C, 
    SpeedRPM, MoveDifferential, MoveTank
from ev3dev2.wheel import EV3Tire
from time import sleep

leftMotor = LargeMotor('outB')
rightMotor = LargeMotor('outC')
tank_drive = MoveTank(OUTPUT_B, OUTPUT_C)

# Arvoja pituuden mittaamista varten
STUD_MM = 8
mdiff = MoveDifferential(OUTPUT_B, OUTPUT_C, EV3Tire, 16 * STUD_MM)

colSens = ColorSensor()
colSens.mode='COL-REFLECT'

def isWhite():
    return colSens.value() > 15
    
def runStraight(speed, distanceMM):
    mdiff.on_for_distance(SpeedRPM(speed), distanceMM)

# Aloita etsimällä valkoinen viiva
while not isWhite():
    tank_drive.run_forever(speed_sp=-100)

# Ohita viiva robotin suoristamista varten
runStraight(-50, 110)

# Käännä robotti viivan suuntaisesti sen ulkopuolella
while not isWhite():
    rightMotor.on(0)
    leftMotor.on(-50)

# Aja ensimmäiselle kiekolle, suorista kulmaa, peruuta hieman ja odota
mdiff.on_for_distance(SpeedRPM(-100), 420)
tank_drive.on_for_degrees(-100, 100, 200) # right turn
mdiff.on_for_distance(SpeedRPM(-100), 20)
time.sleep(8.3)

# Siirry toiselle kiekolle, odota
mdiff.on_for_distance(SpeedRPM(100), 350)
#time.sleep(7.7) # vastapäivään, lyhyt odotus
time.sleep(15) # myötäpäivään, pitkä odotus

# Siirry kolmannelle kiekolle, odota
mdiff.on_for_distance(SpeedRPM(-100), 400)
time.sleep(8)

# Aja ulos viimeiseltä kiekolta kiekolta
mdiff.on_for_distance(SpeedRPM(100), 500)

# Etsi eka valkoinen viiva
while True:
    tank_drive.run_forever(speed_sp=200)
    if isWhite():
        break

# Ensimmäisen valkoisen viivan yli
runStraight(80, 70)

# Etsi toka valkoinen viiva
while True:
    tank_drive.run_forever(speed_sp=200)
    if isWhite():
        break

# Palaa hieman takaisinpäin - etäisyyttä valkoiseen viivaan käännöstä varten
runStraight(-80, 70)

# Käänny valkoiseen reunaan asti
while not isWhite():
    tank_drive.on_for_degrees(100, -100, 25)

# Seuraa valkoista hetki niin saa oikean suunnan
while isWhite():
    leftMotor.on(-100)
    rightMotor.on(-25)

while not isWhite():
    rightMotor.on(-100)
    leftMotor.on(-25)

# Aja maaliin!
runStraight(-100, 800)