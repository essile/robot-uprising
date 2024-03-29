#!/usr/bin/env python3
from ev3dev.ev3 import *
from time import sleep

# Connect EV3 color sensor
cl = ColorSensor()

# Put the color sensor into COL-REFLECT mode
# to measure reflected light intensity.
# In this mode the sensor will return a value between 0 and 100
cl.mode='COL-REFLECT'

while True:
    print(cl.value())
    sleep(0.5)
# I get max 80 with white paper, 3mm separation 
# and 5 with black plastic, same separation